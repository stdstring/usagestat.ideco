create database stat_db;
\connect stat_db
create table stat_storage(id bigserial NOT NULL PRIMARY KEY, source varchar(250) NOT NULL, category varchar(250) NOT NULL, timemarker timestamp NOT NULL, data text not null);
