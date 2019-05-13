# microblog
Sample Flask Project


#### Setup
```shell
 mkdir microblog
 cd microblog
 
 python3 -m venv venv
 
 #virtualenv venv
 source venv/bin/activate
 
 pip install flask
 
 export FLASK_APP=microblog.py  # or pip install python-dotenv and then add .flaskenv file 
 flask run
 ```

 #### Extensions :
 - [Flask-WTF](https://flask-wtf.readthedocs.io/en/stable/)
 ```shell
 pip install flask-wtf
 ```
 - [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) : an extension that provides a Flask-friendly wrapper to the popular SQLAlchemy package, which is an Object Relational Mapper or ORM. SQLAlchemy supports a long list of database engines, including the popular MySQL, PostgreSQL and SQLite.
 ```shell
 pip install flask-sqlalchemy
 ```
 - [Flask-Migrate](https://github.com/miguelgrinberg/flask-migrate) :  This extension is a Flask wrapper for Alembic, a database migration framework for SQLAlchemy. 
 ```shell
 pip install flask-migrate
 ```


#### Learnings :
 - The `form.hidden_tag()` template argument generates a hidden field that includes a token that is used to protect the form against CSRF attacks. All you need to do to have the form protected is include this hidden field and have the `SECRET_KEY` variable defined in the Flask configuration. If you take care of these two things, Flask-WTF does the rest for you.

 - The `flash()`, imported from Flask function is a useful way to show a message to the user.

 - This `redirect()` function instructs the client web browser to automatically navigate to a different page, given as an argument.

 - To have better control over links, Flask provides a function called `url_for()`, which generates URLs using its internal mapping of URLs to view functions. For example, `url_for('login')` returns `/login`, and `url_for('index')` return `/index`. The argument to `url_for()` is the endpoint name, which is the name of the view function.

 - Flask does not support databases natively.

 - The `__repr__` method tells Python how to print objects of this class, which is going to be useful for debugging.
 - __Databases__ :
    ```
    flask db init
    flask db migrate -m "users table"
    flask db upgrade
    ```
    - The upgrade() function applies the migration, and the downgrade() function removes it.
    - Flask-SQLAlchemy uses a "snake case" naming convention for database tables by default. For the User model above, the corresponding table in the database will be named user. For a AddressAndPhone model class, the table would be named address_and_phone. If you prefer to choose your own table names, you can add an attribute named __tablename__ to the model class, set to the desired name as a string.
    - __Database Upgrade and Downgrade Workflow :__  With database migration support, after you modify the models in your application you generate a new migration script (`flask db migrate`), you probably review it to make sure the automatic generation did the right thing, and then apply the changes to your development database (`flask db upgrade`). You will add the migration script to source control and commit it.  
    When you are ready to release the new version of the application to your production server, all you need to do is grab the updated version of your application, which will include the new migration script, and run `flask db upgrade`. Alembic will detect that the production database is not updated to the latest revision of the schema, and run all the new migration scripts that were created after the previous release.  
    As I mentioned earlier, you also have a `flask db downgrade` command, which undoes the last migration. While you will be unlikely to need this option on a production system, you may find it very useful during development. You may have generated a migration script and applied it, only to find that the changes that you made are not exactly what you need. In this case, you can downgrade the database, delete the migration script, and then generate a new one to replace it.
    - It is an unfortunate inconsistency that in some instances such as in a db.relationship() call, the model is referenced by the model class, which typically starts with an uppercase character, while in other cases such as this db.ForeignKey() declaration, a model is given by its database table name, for which SQLAlchemy automatically uses lowercase characters and, for multi-word model names, snake case.
    - The `lazy` argument defines how the database query for the relationship will be issued
    - SQLAlchemy is great in the respect that it provides a high-level abstraction over relationships and foreign keys.
 - `flask shell` : 
    - to start a Python interpreter in the context of the application.
    - second "core" command implemented by Flask, after `run`.
    - With a regular interpreter session, the `app` symbol is not known unless it is explicitly imported, but when using `flask shell`, the command pre-imports the application instance. The nice thing about `flask shell` is not that it pre-imports `app`, but that you can configure a "shell context", which is a list of other symbols to pre-import.
    ```python
    from app import app, db
    from app.models import User, Post

    @app.shell_context_processor
    def make_shell_context():
        return {'db': db, 'User': User, 'Post': Post}
    ```
    - The `app.shell_context_processor` decorator registers the function as a shell context function. When the `flask shell` command runs, it will invoke this function and register the items returned by it in the shell session.



 #### Questions :
 - [Pylint can't find SQLAlchemy query member](https://stackoverflow.com/questions/28193025/pylint-cant-find-sqlalchemy-query-member)
    `pip install pylint-flask`
    Load the installed plugin.
    For example, if you use VS code, please edit setting.json file as follows:
    `"python.linting.pylintArgs": ["--load-plugins", "pylint_flask"]`

 ## Resources :
 - [flask](https://github.com/pallets/flask): The Python micro framework for building web applications. https://www.palletsprojects.com/p/flask/
 - [The Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
 - [Flask-WTF](https://flask-wtf.readthedocs.io/en/stable/) : Simple integration of Flask and WTForms, including CSRF, file upload, and reCAPTCHA.
