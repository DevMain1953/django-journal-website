## About project

Scientific journal website, entities in database are made simpler to reduce development complexity.

TODOs / code refactoring:
- reduce number of lines of code in ```views.py``` (move the request handling functionality to specific class);
- remove warnings in logs about using unordered list of objects (QuerySet) for pagination in templates;
- replace pks with ids for queries to database in repositories;
- change SQLite to PostgreSQL.

## How to install and run

- clone this repository using `git clone <link>` command
- you need docker to be installed, run the command below, this will download all necessary images and build current application image with all dependencies.
```
docker compose up
```