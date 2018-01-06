# EVote

### Database
For a vast amount of information on how Django implements databases and on how to perform queries please refer to the Django docs.

https://docs.djangoproject.com/en/2.0/ref/databases/

https://docs.djangoproject.com/en/2.0/topics/db/queries/

Django uses mysql stored in \website\db.sqlite3. If no such file exists then run.
> python manage.py migrate --run-syncdb

If you want to purge the entire database

> delete db.sqlite3

> delete everything in website\vote\migrations

> run the syncdb command above

Django implements the database manipulation using an object oriented paradigm.
_models.py_ contains information on the data models used in EVote.

_queries.py_ contains direct data model manipulation (Not just queries).

The Entity Relationship Diagram (ERD) is located in a gliffy file in the root folder.
In order to open the file

> Install Google Chrome

> Go to the Google Chrome App Store

> Install "Gliffy Diagrams"

EVote's database model stores not only information about the current election, but also all past elections. It also maintains a database of faculty that have participated in elections, whether they were nominees or voters. Currently there is no way of obtaining tokens from old elections so the only solution is to hold on to important tokens or implement the functionality.
