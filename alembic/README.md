Generic single-database configuration.

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