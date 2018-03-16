CREATE TABLE apireleas(
  buildtime date,
  version varchar(30) primary key,
  links varchar2(30),
  methods varchar2(30)
);

INSERT INTO apireleas values(current_timestamp,"v1","/api/v1/users","get, post, put, delete");

select * from apireleas;