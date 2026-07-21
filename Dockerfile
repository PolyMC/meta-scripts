FROM python:3.12.4-bullseye
ARG UID=1337
ARG GID=1337

RUN groupadd -g $GID user \
    && useradd -m -g $GID -u $UID user \
    && mkdir -p /home/user/.ssh \
    && ssh-keyscan github.com > /home/user/.ssh/known_hosts \
    && mkdir -p /app \
    && chown -R $UID:$GID /app /home/user/.ssh

COPY . /app/

RUN pip install -r /app/requirements.txt \
    && apt-get update && apt-get install -y rsync cron openssh-client

# add our cronjob
COPY docker/update.cron /etc/cron.d/meta-update
RUN chmod 644 /etc/cron.d/meta-update \
    && crontab /etc/cron.d/meta-update

# install entrypoint
COPY docker/entrypoint.sh /usr/local/bin/entrypoint
RUN chmod +x /usr/local/bin/entrypoint

ENTRYPOINT ["/usr/local/bin/entrypoint"]
CMD ["update"]
