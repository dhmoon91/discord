## Running:

1. Ping stanley for env variables;
2. Create **.env** file on root directory with following:

```
RIOT_API_KEY={APIKEY}
DISCORD_TOKEN={TOKEN}
```

3. Install required pip library:
   ` pip3 install -r requirements.txt`
4. Run `npx nodemon --exec python3 bot.py`
5. IF ^ fails, `python3 bot-main.py`
6. We use `black` as auto formatter.

- Install `black`; pip3 install black
- Set `Python › Formatting: Provider` in vscode setting to be `black`.
- **If you have prettier setup, you have to override it**:
  - Open language specific setting in vscode for python(CMD + SHIFT + P)
  - Add this line in
  ```
  [python]:{
     ...
      "editor.defaultFormatter": "ms-python.python"
  }
  ```
- This will set up auto formatting upon saving a file.

7. To enable `pylint` on `pre-push`, please run following command:
```
pre-commit install --hook-type pre-push
```

8. To call the bot with the desired prefix locally, 

- Add `LOCAL_BOT_PREFIX= ""` to .env with desired prefix between the double quotes

9. Install Postgresql server 9.6.2 or up brew install postgresql and start it brew services start postgresql
Initialize development and test databases as described below:
Use following command to bootstrap dev databases
```
$ psql postgres
postgres=# CREATE USER admin_bot WITH SUPERUSER PASSWORD 'test';
postgres=# CREATE DATABASE bot_dev OWNER admin_bot;
```

10. DB Migration and setup:
Base ORM and DB engine; `SQLAlchemy` and `psycopg2`
- Install both `SQLAlchemy`, `psycopg2` if you haven't from step `3`.
- Add `DB_URL='postgresql://admin_bot:test@localhost/bot_dev'` into .env file
- ## Migrations
   * Uses https://alembic.sqlalchemy.org/

   * Install alembic if not installed yet from step `3`  
   `pip3 install alembic`

   * For first time, after install, run   
   `alembic upgade head`
   
   * To genearte new migration;  
   `alembic revision -m "create account table"`  
   This will create new migration file under /alembic/versions. Fill in the file.
   
   * To apply migration;  
   `alembic upgrade head`

   * **Make sure you update the models reference in db/models/ to represent newly added schema**

   * To revert one migration;  
   `alembic downgrade -1`

   * To revert all migration;  
   `alembic downgrade base`
## Packages:

**Pydash**
https://pydash.readthedocs.io/en/latest/index.html

**riotwatcher**
https://riot-watcher.readthedocs.io/en/latest/
