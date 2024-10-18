
To build the containers:
1. pull the branch
2. cd to App folder. Make sure docker-compose.yml file is in the folder you are in.
3. run: docker compose up

Docker will build images and create running containers. 

Next, you will need to create tables and add data to them. Steps to do that are in init-data folder.

Once the database is populated, you can check how endpoints are responding.

To check the running containers from the command line, run: docker ps.
To get IP addresses of each container, run: docker network inspect app_idb. Each container will have its own IP address starting from 172.<>.<>.<>

To test the API from the container: in the web app container terminal run curl "http://\<IP address of the app.py\>:\<connected port\>/predict"
or curl "http://\<IP address of PostgREST\>:\<connected port\>/\<table name in the database\>". 

You can access the container via its name. Database is accessed through the PostgREST interface, instead of IP address, you can use app-server-1:\<port\>. Instead of IP address of backend, you can use app-backend-1:\<port\>.

