1. Ensure the `geography` table is exist in the Database
2. Run below command to seed world data into geography table
```sh

docker exec -it -w /app/db/scripts/geography app-server python seed_geography.py

```
