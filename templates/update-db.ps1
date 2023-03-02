# Updates local database
dotnet run --project .\{PROJECT_NAME}.Database.csproj -- "Host=localhost; User Id=postgres; Password=postgres; Database={PROJECT_NAME_LOWER_CASE}db; Port=50000"