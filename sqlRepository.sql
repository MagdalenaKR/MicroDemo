CREATE TABLE apireleas(
  buildtime date,
  version varchar(30) primary key,
  links varchar2(30),
  methods varchar2(30)
);

INSERT INTO apireleas values(current_timestamp,"v1","/api/v1/users","get, post, put, delete");

CREATE TABLE users(
username varchar2(30),
emailid varchar2(30),
password varchar2(30), full_name varchar(30),
id integer primary key autoincrement);