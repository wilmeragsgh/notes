---
description: Frequently used code for postgresql
---

# Postgresql

## Recipes

**Installing - Ubuntu**

```bash
sudo apt-get install wget ca-certificates
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" >> /etc/apt/sources.list.d/pgdg.list'
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
```

**Installing - Docker**

```bash
docker run --name pg_docker \
    -p 5432:5432 \
    -e POSTGRES_DB=db-name \
    -e POSTGRES_PASSWORD=pass \
    -d postgres
    
# Access from host
psql -h localhost -p 5432 -d db-name -U postgres --password
```



**Execute commands from current user (without user on db)**

```sh
echo "\d" | sudo -u postgres psql
```

**Create database**
```sql
CREATE DATABASE phishiq_db;
```

**Create user**
```sql
CREATE USER user PASSWORD 'pass';
```

**Grant privilage to such user**

```sql
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO user;
ALTER ROLE user SUPERUSER;
ALTER ROLE user CREATEDB; 
ALTER ROLE user WITH LOGIN;
```

**Create table**
```sql
CREATE TABLE tbl([col [type]]...)
```

**List db**
`\d`

**List users**
`
\du
`

**Change user password**
```SQL
ALTER USER davide WITH PASSWORD 'hu8jmn3';
```

**List constraint for a table**
```SQL
\d+ tablename
```

**Create constraint**
```SQL
ALTER TABLE raw_backup ADD CONSTRAINT raw_backup_pk UNIQUE (ticker, period, date);
```

**Create index**
```SQL
CREATE INDEX idx_date_backup ON raw_backup(date);
```

**Remove constraint**
```SQL
ALTER TABLE affiliations
DROP CONSTRAINT affiliations_organization_id_fkey;
```

**Generating dump file**

```bash
pg_dump -U postgres --schema-only db_name > file.txt
```

**Loading dump file**

```bash
psql -U username dbname < dbexport.pgsql
```