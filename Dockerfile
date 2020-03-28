FROM python:3.8-slim

ENV PYTHONUNBUFFERED 1
WORKDIR /app

COPY requirements.txt ./
RUN set -ex \
	&& buildDeps=" \
		build-essential \
		libssl-dev \
		libgmp-dev \
		pkg-config \
		" \
    && apt-get update \
    && apt-get install -y --no-install-recommends $buildDeps \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y --auto-remove $buildDeps \
    && rm -rf /var/lib/apt/lists/* \
    && find /usr/local \
        \( -type d -a -name test -o -name tests \) \
        -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
        -exec rm -rf '{}' +

# Create a use with no privileges:
# - Creates a system user (-r), with no password, no home directory set, and no shell
# - Adds the user we created to an existing group that we created beforehand (using groupadd)
# - Adds a final argument set to the user name we want to create, in association with the group we created
# https://snyk.io/blog/10-docker-image-security-best-practices/
RUN groupadd -r -g 1000 monitor
RUN useradd -r -s /bin/false -g 1000 -u 1000 monitor
RUN chown -R 1000:1000 /app

# Signal handling for PID1 https://github.com/krallin/tini
ENV TINI_VERSION v0.18.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini

COPY . .

# Change user
USER 1000

ENTRYPOINT ["/tini", "--"]
