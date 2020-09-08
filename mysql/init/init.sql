# GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;
# CREATE DATABASE traineeboats;
-- auto-generated definition
create table dim_vessel
(
    mmsi int                       not null
        primary key,
    imo  int                       null,
    name varchar(255) charset utf8 null,
    type varchar(255) charset utf8 null
);

