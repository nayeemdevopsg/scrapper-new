FROM python:3.9


WORKDIR /app


COPY . /app


RUN pip install -r requirements.txt

RUN apt-get update && \
    apt-get install -y wget gnupg unzip && \
    apt-get clean

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list


RUN apt-get update -y
RUN apt-get install -y google-chrome-stable


RUN wget -qP /usr/local/bin "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/121.0.6167.85/linux64/chromedriver-linux64.zip" && \
    unzip /usr/local/bin/chromedriver-linux64.zip -d /usr/local/bin && \
    rm /usr/local/bin/chromedriver-linux64.zip && \
    mv /usr/local/bin/chromedriver-linux64/chromedriver /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver

EXPOSE 80

ENTRYPOINT ["gunicorn", "--workers=4","--timeout", "3600", "--bind", "0.0.0.0:80", "scraper.wsgi:application"]
