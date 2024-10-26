CREATE DATABASE homefinance;
USE homefinance;
CREATE TABLE user(
   id int primary key auto_increment,
   name_user varchar(60) NOT NULL,
   email_user varchar(60) NOT NULL,
   password_user char(8) NOT NULL    
);

CREATE TABLE level(
   id int primary key auto_increment,
   name_level varchar(50) NOT NULL
);

CREATE TABLE despesas (
   id INT PRIMARY KEY AUTO_INCREMENT,
   valor DECIMAL(10, 2) NOT NULL,  
   data DATE NOT NULL,              
   tipo VARCHAR(50) NOT NULL,   
   nome VARCHAR(50) NOT NULL,     
   usuario_id INT,                  
   FOREIGN KEY (usuario_id) REFERENCES user(id)  
);


ALTER TABLE user
ADD COLUMN level_id INT,
ADD CONSTRAINT fk_user_level
FOREIGN KEY (level_id) REFERENCES level(id);

select * from user;
select * from level;
select * from despesas;

DELETE FROM despesas
WHERE usuario_id IS NULL;

