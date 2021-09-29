CREATE TABLE foods (
   id INTEGER UNIQUE,
   name TEXT NOT NULL,
   country TEXT NOT NULL,
   continent TEXT NOT NULL,
   tastes TEXT NOT NULL,
   hardness TEXT NOT NULL,
   temp TEXT NOT NULL,
   ingredients TEXT NOT NULL,
   description TEXT NOT NULL,
   image TEXT NOT NULL,
   PRIMARY KEY(id));