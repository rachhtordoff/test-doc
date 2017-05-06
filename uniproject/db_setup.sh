#!/usr/bin/env bash
#   Use this script to setup your database


#docker cp /vagrant/.postgres_init.sql postgres:/postgres_init.sql

#docker exec postgres psql -q -f '/postgres_init.sql

#create users
docker exec uniproject_postgres_1 psql --command "CREATE USER Optiself_user WITH SUPERUSER PASSWORD 'password';"

#create databases
docker exec uniproject_postgres_1 psql --command "CREATE DATABASE Optiself_user OWNER Optiself_user;"

#setup databases
docker exec uniproject_secure_api_1 python3 db_scripts/db_create.py
