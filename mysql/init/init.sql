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

DROP TABLE IF EXISTS fact_ais;
CREATE TABLE fact_ais
(
    id              int primary key auto_increment,
    timestamp       varchar(64),
    mobile_status   varchar(64),
    mmsi            varchar(64),
    latitude        varchar(64),
    longitude       varchar(64),
    nav_status      varchar(64),
    rot             varchar(64),
    sog             varchar(64),
    cog             varchar(64),
    heading         varchar(64),
    imo             varchar(64),
    callsign        varchar(64),
    position_device varchar(64),
    destination     varchar(64),
    eta             varchar(64),
    source_type     varchar(64),
    hash            varchar(700) unique
);