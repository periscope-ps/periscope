drop database if exists periscopedb;
CREATE DATABASE periscopedb CHARACTER SET utf8;
GRANT USAGE on *.* to periuser@localhost IDENTIFIED BY 'peri2pass';
grant all privileges on periscopedb.* to periuser@localhost ;
