docker-compose file contains database name that is created when containers are built.

To add data to database app_db: 
1. open Postgres terminal in a running container
2. cd to /var/lib/postgresql@17
2. run: 
psql "host=localhost port=5432 dbname=app_db user=app_user password=password" -f create_table.sql
psql "host=localhost port=5432 dbname=app_db user=app_user password=password" -f import.sql
These 2 commands will create a table with device name provided in sql file and import the data from csv you add to the init-data folder.
3. Check the data from Postgres container: 
- get into db: psql "host=localhost port=5432 dbname=app_db user=app_user password=password"
- inside the db: select * from public.device_1;
4. Check the data from REST interface:
- check the ip address assigned for the PostgREST container: docker network inspect app_idb
- run the command: curl "http://app-server-1:3000/<table name>" where app-server-1 is a container name OR you can use ip adress instead of the container name
- in the browser: http://\<ip address of postgrest server\>:3000/<table name>
