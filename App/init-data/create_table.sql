-- This is a possible way to create a table for each device
-- Please note that table columns are not required to be named like that or have datatype as below
DROP TABLE IF EXISTS public.device_1;
CREATE TABLE public.device_1 (
  id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  time_data VARCHAR(255),
  temp REAL,
  compStat VARCHAR(50)
);
-- This part os the file is needed to create anonymous REST API calls using PostgREST interface
CREATE ROLE web_anon nologin;

GRANT usage ON SCHEMA public TO web_anon;
GRANT SELECT ON public.device_1 TO web_anon;
GRANT web_anon to app_user;



