## About project

Scientific journal website, entities in database are made simpler to reduce development complexity. Website allows authors publish their articles in ```docx``` format, application will automatically process the file and save main attributes of article to database in two languages if it's possible. For reviewers, application allows to read articles and give feedbacks to authors. When feedback is posted, author receives email message with link to it. If article has more positive feedbacks than negative ones, status of article will be "Accepted".

TODOs / code refactoring:
- reduce number of lines of code in ```views.py``` (move the request handling functionality to specific class) **OR** in case of context change, replace function based views with class based views;
- remove warnings in logs about using unordered list of objects (QuerySet) for pagination in templates;
- test the replacing ```pks``` with ```ids``` for queries to database in repositories and views because of [this](https://stackoverflow.com/a/53100893/11152224);
- add ```__init__.py``` to repositories and managers;
- change SQLite to PostgreSQL.

## How to install and run

- clone this repository using `git clone <link>` command
- you need docker to be installed, run the command below, this will download all necessary images and build current application image with all dependencies.
```
docker compose up
```