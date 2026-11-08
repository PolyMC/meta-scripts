FROM python:3.15-slim

ARG UID=1337
ARG GID=1337
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends git openssh-client \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd -g "$GID" meta \
    && useradd -m -u "$UID" -g "$GID" meta

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY meta meta
COPY static static

USER meta
RUN mkdir -p /home/meta/.ssh && ssh-keyscan github.com > /home/meta/.ssh/known_hosts

ENTRYPOINT ["python", "-m", "meta"]
