-- this will drop or delete the database;
drop database if exists EmployeeDatabase;
create database EmployeeDatabase;
use EmployeeDatabase;

Create table Employee(
EMPID    	VarChar(4) primary key,
Gender	 	VarChar(1),
Age      	int(2),
Sales 		int(3),
BMI         VarChar(11),
Salary      int(3),
Birthday    date
);