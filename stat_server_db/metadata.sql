drop database if exists stat_db;
create database stat_db;
\connect stat_db
create table stat_storage(id bigserial NOT NULL PRIMARY KEY, user_id uuid NOT NULL, source varchar(250) NOT NULL, category varchar(250) NOT NULL, timemarker timestamp NOT NULL, data text NOT NULL);
