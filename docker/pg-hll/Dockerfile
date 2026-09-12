FROM postgres:16

# Install hll extension package
RUN apt-get update \
    && apt-get install -y postgresql-16-hll \
    && rm -rf /var/lib/apt/lists/* \
    