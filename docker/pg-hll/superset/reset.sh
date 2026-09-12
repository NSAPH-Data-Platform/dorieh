#!/bin/bash

docker container ls -a | grep super | awk '{print $1}' | xargs docker container rm -f
docker container rm -f pg-hll-redis-1
docker volume rm pg-hll_superset_home
docker volume rm pg-hll_redis_data

docker compose -f docker-compose-superset.yml up --build
