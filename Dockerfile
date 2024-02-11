# Use the Python 3.9 base image
FROM python:3.9

# Set working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Python dependencies
RUN pip install -r requirements.txt

# Update package lists and install necessary packages
RUN apt-get update && \
  apt-get install -y wget gnupg unzip && \
  apt-get clean

# Download and install specific version of ChromeDriver
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
# Update the package list and install chrome
RUN apt-get update -y
RUN apt-get install -y google-chrome-stable
# Set up Chromedriver Environment variables
#ENV CHROMEDRIVER_VERSION 97.0.4692.71

#RUN wget -qP /usr/local/bin "https://chromedriver.storage.googleapis.com/114.0.5735.16/chromedriver_linux64.zip" && \  
RUN wget -qP /usr/local/bin "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/121.0.6167.85/linux64/chromedriver-linux64.zip" && \
 unzip /usr/local/bin/chromedriver-linux64.zip -d /usr/local/bin && \
 rm /usr/local/bin/chromedriver-linux64.zip && \
 mv /usr/local/bin/chromedriver-linux64 /usr/local/bin/chromedriver && \
 chmod +x /usr/local/bin/chromedriver

EXPOSE 80
# Command to run the application with Gunicorn
ENTRYPOINT ["gunicorn", "--workers=4","--timeout", "3600", "--bind", "0.0.0.0:80", "scraper.wsgi:application"]

