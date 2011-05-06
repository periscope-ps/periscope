DROP DATABASE IF EXISTS periscopedb;
CREATE DATABASE periscopedb CHARACTER SET utf8;
GRANT USAGE on *.* to periuser@localhost IDENTIFIED BY 'peri2pass';
GRANT ALL privileges on periscopedb.* to periuser@localhost;
