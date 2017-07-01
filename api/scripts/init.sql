create table test (varchar varchar(50), datetime  datetime default CURRENT_TIMESTAMP);
insert into test (varchar) values ('hello world!');
select * from test;
