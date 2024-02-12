# --------- Base --------

FROM fedora:39 as base

ARG UID
ARG GID
ENV APP_USER=nonroot
COPY google-chrome-stable_current_x86_64.rpm google-chrome-stable_current_x86_64.rpm

RUN set -eux ;\
    groupadd -g ${GID} ${APP_USER} && \
    useradd -u ${UID} -g ${GID} -m ${APP_USER} ;\
    dnf -y --allowerasing --nodocs --setopt install_weak_deps=False upgrade && dnf4 clean all ;\
    dnf -y --allowerasing --nodocs --setopt install_weak_deps=False autoremove && dnf4 clean all ;\
    dnf install -y --allowerasing --nodocs python3-pip libpq-devel && dnf4 clean all ;\
    dnf install -y --allowerasing --nodocs ./google-chrome-stable_current_x86_64.rpm && dnf4 clean all ;\
    pip install --no-cache --upgrade pip setuptools wheel ;\
    dnf clean all ;\
    rm -rf google-chrome-stable_current_x86_64.rpm ;\
    ln /usr/bin/python3 /usr/bin/python ; \
    chown -R ${APP_USER}:${APP_USER} /home/${APP_USER} && chmod -R 775 /home/${APP_USER} ;\
    chown -R ${APP_USER}:${APP_USER} /var/run/ && chmod -R 775 /var/run/ ;

# --------- Base --------

# --------- Build --------
FROM base as build

RUN set -eux ;\
    pip install --no-cache --upgrade pip setuptools wheel ;

USER ${APP_USER}
WORKDIR /home/${APP_USER}
COPY requirements.txt /home/${APP_USER}/requirements.txt

# install dependency
RUN set -eux ;\
    python -m venv venv ;\
    source venv/bin/activate && \
    pip install --no-cache --upgrade pip setuptools wheel ;\
    pip wheel --no-cache -r requirements.txt -w wheelhouse ;

# --------- Build --------

# --------- Final --------

FROM base as final

EXPOSE 8000
USER ${APP_USER}
WORKDIR /home/${APP_USER}
COPY --chown=${UID}:${GID} --chmod=775 temp_copy /home/${APP_USER}/project/

# Copy wheel files from the build stage
COPY --from=build --chown=${UID}:${GID} --chmod=775 /home/${APP_USER}/wheelhouse /home/${APP_USER}/wheelhouse

# Install dependency
RUN set -eux ;\
    pip install --no-cache --no-index --no-warn-script-location --find-links=/home/${APP_USER}/wheelhouse -r /home/${APP_USER}/project/requirements.txt ;\
    rm -rf wheelhouse ;

# Fix dramatiq executable not found error


ENTRYPOINT ["./project/entrypoint.sh"]

# --------- Final --------
