drop database if exists stat_db_source_test;
create database stat_db_source_test;
\connect stat_db_source_test
create table main_data_storage(id serial NOT NULL PRIMARY KEY, user_id uuid NOT NULL, data_part1 varchar(100) NOT NULL, data_part2 varchar(100) NULL, data_part3 varchar(100) NULL);
create table user_data_storage(user_id uuid NOT NULL PRIMARY KEY, user_data varchar(100) NOT NULL);
