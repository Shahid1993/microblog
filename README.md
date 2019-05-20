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
 - [Flask-Login](https://flask-login.readthedocs.io/en/latest/) : Flask-Login provides user session management for Flask. It handles the common tasks of logging in, logging out, and remembering your users’ sessions over extended periods of time.
   ```shell
   pip install flask-login
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
 - __Password Hashing :__
    - One of the packages that implement password hashing is [Werkzeug](https://palletsprojects.com/p/werkzeug/) - pre-installed as it is one of the core dependencies of Flask
      ```python
      >>> from werkzeug.security import generate_password_hash
      >>> hash = generate_password_hash('foobar')
      >>> hash
      'pbkdf2:sha256:50000$vT9fkZM8$04dfa35c6476acf7e788a1b5b3c35e217c78dc04539d295f011f01f18cd2175f'
      ```
    - verification :
      ```python
      >>> from werkzeug.security import check_password_hash
      >>> check_password_hash(hash, 'foobar')
      True
      >>> check_password_hash(hash, 'barfoo')
      False
      ```
 - __Flask-Login__ needs to be created and initialized right after the application instance in _app/__init__.py_. 
    - The Flask-Login extension works with the application's user model, and expects certain properties and methods to be implemented in it.
    - The four required items are listed below:
        - `is_authenticated`: a property that is `True` if the user has valid credentials or `False` otherwise.
        - `is_active`: a property that is `True` if the user's account is active or `False` otherwise.
        - `is_anonymous`: a property that is `False` for regular users, and `True` for a special, anonymous user.
        - `get_id()`: a method that returns a unique identifier for the user as a string (unicode, if using Python 2)
    - Since the implementations are fairly generic, Flask-Login provides a mixin class called UserMixin that includes generic implementations that are appropriate for most user model classes.
      ```python
      # ...
      from flask_login import UserMixin

      class User(UserMixin, db.Model):
         # ...
      ```
    - Flask-Login keeps track of the logged in user by storing its unique identifier in Flask's user session, a storage space assigned to each user who connects to the application. Each time the logged-in user navigates to a new page, Flask-Login retrieves the ID of the user from the session, and then loads that user into memory.
    - Because Flask-Login knows nothing about databases, it needs the application's help in loading a user. For that reason, the extension expects that the application will configure a user loader function, that can be called to load a user given the ID.
    - The `is_anonymous` property is one of the attributes that Flask-Login adds to user objects through the `UserMixin` class. The `current_user.is_anonymous` expression is going to be `True` only when the user is not logged in.
    - __Requiring Users To Login :__ Flask-Login provides a very useful feature that forces users to log in before they can view certain pages of the application. 
        - For this feature to be implemented, Flask-Login needs to know what is the view function that handles logins. 
         ```python
         # ...
         login = LoginManager(app)
         login.login_view = 'login'
         ```
        - The way Flask-Login protects a view function against anonymous users is with a decorator called `@login_required`. When you add this decorator to a view function below the `@app.route` decorators from Flask, the function becomes protected and will not allow access to users that are not authenticated.

 - When you add any methods that match the pattern `validate_<field_name>`, WTForms takes those as custom validators and invokes them in addition to the stock validators. 

 - `first_or_404()` : works exactly like first() when there are results, but in the case that there are no results automatically sends a 404 error back to the client.

 - [__Gravatar__](https://en.gravatar.com/) : To request an image for a given user, a URL with the format https://www.gravatar.com/avatar/<hash>, where <hash> is the MD5 hash of the user's email address.
   ```shell
   >>> from hashlib import md5
   >>> 'https://www.gravatar.com/avatar/' + md5(b'john@example.com').hexdigest()
   'https://www.gravatar.com/avatar/d4c74594d841139328695756648b6bd6'
   ```

- __Using Jinja2 Sub-Templates__ : To invoke sub-template, use Jinja2's `include` statement:
   ```python
   {% for post in posts %}
      {% include '_post.html' %}
   {% endfor %}
   ```

- The `@before_request` decorator from Flask register the decorated function to be executed right before the view function.

- __Debug Mode :__ To activate debug mode, stop the application, and then set the following environment variable:
   ```shell
   export FLASK_DEBUG=1
   ```
   or set `FLASK_DEBUG=1` in _.flaskenv_ file
   - It is extremely important that you never run a Flask application in debug mode on a production server. The debugger allows the user to remotely execute code in the server.
   - _reloader_ feature is also enabled with debug mode.

- __Custom Error Pages :__ To declare a custom error handler, the `@errorhandler` decorator is used.

- __Sending Errors by Email :__ 
   - The first step is to add the email server details to the configuration file:
      ```python
      class Config(object):
         # ...
         MAIL_SERVER = os.environ.get('MAIL_SERVER')
         MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
         MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
         MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
         MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
         ADMINS = ['your-email@example.com']
      ```
   - Flask uses Python's `logging` package to write its logs, and this package already has the ability to send logs by email. All I need to do to get emails sent out on errors is to add a SMTPHandler instance to the Flask logger object, which is `app.logger`:
      ```python
      import logging
      from logging.handlers import SMTPHandler

      # ...

      if not app.debug:
         if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                  auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                  secure = ()
            mail_handler = SMTPHandler(
                  mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                  fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                  toaddrs=app.config['ADMINS'], subject='Microblog Failure',
                  credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)
      ```

   - There are two approaches to test this feature. 
      - The easiest one is to use the SMTP debugging server from Python. This is a fake email server that accepts emails, but instead of sending them, it prints them to the console. To run this server, open a second terminal session and run the following command on it:
         ```shell
         python -m smtpd -n -c DebuggingServer localhost:8025
         ```
      - A second testing approach for this feature is to configure a real email server. Below is the configuration to use your Gmail account's email server:
         ```shell
         export MAIL_SERVER=smtp.googlemail.com
         export MAIL_PORT=587
         export MAIL_USE_TLS=1
         export MAIL_USERNAME=<your-gmail-username>
         export MAIL_PASSWORD=<your-gmail-password>
         ```

   - __Logging to a File :__ To enable a file based log another handler, this time of type RotatingFileHandler, needs to be attached to the application logger, in a similar way to the email handler.
      ```python
      # ...
      from logging.handlers import RotatingFileHandler
      import os

      # ...

      if not app.debug:
         # ...

         if not os.path.exists('logs'):
            os.mkdir('logs')
         file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
                                             backupCount=10)
         file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
         file_handler.setLevel(logging.INFO)
         app.logger.addHandler(file_handler)

         app.logger.setLevel(logging.INFO)
         app.logger.info('Microblog startup')
      ```





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
