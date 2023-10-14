DROP TABLE IF EXISTS public.row_parser;
create table IF NOT EXISTS public.row_parser (
link_resume text PRIMARY KEY,
job_title text,
salary text,
age text,
family_status text,
city text,
readiness_to_move text,
employment text,
citizenship text,
professional_skill text,
years_of_experience text,
experience  text,
education text,
foreign_language  VARCHAR (100),
drivers_license  VARCHAR (100),
additional_information text
);

  --id int, 
  --first_name text, 
  --last_name text, 
  --department_id int, 
  --salary numeric, 
  --years_worked int


DROP TABLE IF EXISTS public.ods_parser;
create table IF NOT EXISTS public.ods_parser (
dws_job VARCHAR (100),
insert_date timestamp,
system VARCHAR (100),
date timestamp,
link_resume text PRIMARY KEY,
job_title text,
salary text,
age text,
family_status text,
city text,
readiness_to_move text,
employment text,
citizenship text,
professional_skill text,
years_of_experience text,
experience  text,
education text,
foreign_language  VARCHAR (100),
drivers_license  VARCHAR (100),
additional_information text
);

DROP TABLE IF EXISTS public.ods_parser;
create table IF NOT EXISTS public.ods_parser (
dws_job VARCHAR (100),
insert_date timestamp,
system_id int,
date timestamp,
id_lr text PRIMARY KEY, ---
link_resume1 text,
job_title text,
salary text,
age text,
family_status text,
city text,
readiness_to_move text,
employment text,
citizenship text,
professional_skill text,
years_of_experience text,
experience  text,
education text,
foreign_language  VARCHAR (100),
drivers_license  VARCHAR (100),
additional_information text
);