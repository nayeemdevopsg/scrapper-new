FROM python:3.9

# Set working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Update package lists and install necessary packages
RUN apt-get update && \
  apt-get install -y wget gnupg unzip && \
  apt-get clean

# Install Google Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
  echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
  apt-get update && \
  apt-get install -y google-chrome-stable && \
  rm -rf /var/lib/apt/lists/*

# Download and install ChromeDriver
RUN CHROMEDRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE) && \
  wget -qP /usr/local/bin "http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip" && \
  unzip /usr/local/bin/chromedriver_linux64.zip -d /usr/local/bin && \
  rm /usr/local/bin/chromedriver_linux64.zip && \
  chmod +x /usr/local/bin/chromedriver

# Expose port 8000 to the outside world
EXPOSE 8080

# Command to run the application with Gunicorn
CMD ["gunicorn", "--workers=4", "--bind", "0.0.0.0:8080", "scraper.wsgi:application"]