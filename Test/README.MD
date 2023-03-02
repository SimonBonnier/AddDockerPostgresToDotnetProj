Hello there

## Connect to docker Postgresql db from commandline
1. Get running container name with: docker ps
2. docker exec -it {container_name} bash
3. psql -U {user_name} -W (type pasword)
4. \l (list all databases)
5. \c {db_name} (type pasword)
6. \d (list all tables)

