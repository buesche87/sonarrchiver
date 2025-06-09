FROM python:3.11-slim

# Install cron and clean up
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy files
COPY app/script.py /app/script.py

# Install requests
RUN pip install requests urllib3

# Create log file
RUN touch /var/log/cron.log

# Run cron and log output
CMD sh -c 'echo "$CRON_SCHEDULE root python /app/script.py >> /var/log/cron.log 2>&1" > /etc/cron.d/sonarr-cronjob && \
    chmod 0644 /etc/cron.d/sonarr-cronjob && \
    crontab /etc/cron.d/sonarr-cronjob && \
    (sleep 180 && python /app/script.py) & \
    cron && tail -f /var/log/cron.log'