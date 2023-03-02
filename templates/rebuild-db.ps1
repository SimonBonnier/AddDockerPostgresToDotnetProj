# Updates local database
docker exec -it {PROJECT_NAME_LOWER_CASE}_db_1 bash -c "psql -U postgres -w postgres -c 'DROP DATABASE {PROJECT_NAME_LOWER_CASE}db;'";
docker exec -it {PROJECT_NAME_LOWER_CASE}_db_1 bash -c "psql -U postgres -w postgres -c 'CREATE DATABASE {PROJECT_NAME_LOWER_CASE}db;'";

dotnet run --project .\{PROJECT_NAME}.Database.csproj -- "Host=localhost; User Id=postgres; Password=postgres; Database={PROJECT_NAME_LOWER_CASE}db; Port=50000"