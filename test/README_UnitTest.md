HOW TO RUN UNIT TEST

1. Setup unittest DB
```
$ psql postgres
postgres=# CREATE USER admin_bot WITH SUPERUSER PASSWORD 'test';
postgres=# CREATE DATABASE unittest OWNER admin_bot;
```
Update `DB_URL` to be `'postgresql://admin_bot:test@localhost/unittest'` in `.env` file
Run following commands in /discord folder:
```
pip3 install alembic
alembic upgade head
```
Now the unittest DB setup should be completed

Revert back `DB_URL` to be `postgresql://admin_bot:test@localhost/bot_dev` for your dev tests
Add `TEST_DB_URL='postgresql://admin_bot:test@localhost/unittest'` in `.env` file


2. Run test with following command
```
pytest -v test/test_get_rank.py
```
