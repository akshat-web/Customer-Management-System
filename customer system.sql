create database customer;
use customer;
create table basic_information(customer_ID varchar(255), first_name varchar(255),last_name varchar(255),age varchar(255),gender varchar(255),primary key(customer_ID));
create table contacts(customer_ID varchar(255),phone varchar(255),email varchar(255),address varchar(255),primary key(customer_ID));
create table preference(customer_ID varchar(255),most_bought varchar(255), least_bought varchar(255),primary key(customer_ID));
create table payment(customer_ID varchar(255),cash varchar(255),card varchar(255),UPI varchar(255),primary key(customer_ID));
create table admin(username varchar(255),password varchar(255),primary key(username));
create table complaints(customer_ID varchar(255),complaint varchar(255),is_resolved varchar(255),primary key(customer_ID));
create table sales(customer_ID varchar(255),clothes int,foods int,electronics int,furniture int,make_up int,primary key(customer_ID));
create table feedback(username varchar(255) primary key,names varchar(255),review varchar(255));
insert into basic_information values('C3411','Joe','Pre','35','male');
insert into contacts values('C0112','1110864566','yeah@gmail.com','44,Asria,Birminghamon');
insert into preference values('C12313','foods','clothes');
insert into payment values('C0112','never','never','always');
insert into admin values('ff011','april');
insert into complaints values('C2222','wrong item received','yes');
insert into sales values('C3411',3451,200,3304,1341,321);
update sales set overall_purchase= 100000 where customer_ID='C3411';
delete from preference where customer_ID='C012313';
delete from feedback where username = 'mupple11';
alter table feedback drop column username;
alter table feedback add column customer_ID varchar(255) primary key;
select * from basic_information;
select*from feedback;