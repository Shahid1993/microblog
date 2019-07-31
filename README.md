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
 - [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) : an extension that provides a Flask-friendly wrapper to the popular SQLAlchemy package, which is an Object Relational Mapper or ORM. SQLAlchemy supports a long list of database engines, including the popular MySQL, PostgreSQL and SQLite (simple and does not require a server). 
   ORMs allow applications to manage a database using high-level entities such as classes, objects and methods instead of tables and SQL. The job of the ORM is to translate the high-level operations into database commands.
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
 - [Flask-Mail](https://pythonhosted.org/Flask-Mail/) : provides a simple interface to set up SMTP with your Flask application and to send messages from your views and scripts.
   ```shell
   pip install Flask-Mail
   ```
 - [JSON Web Tokens](https://jwt.io/) : an open, industry standard RFC 7519 method for representing claims securely between two parties. JWT.IO allows you to decode, verify and generate JWT.
   ```shell
   pip install pyjwt
   ```
 - [Flask-Bootstrap](https://pythonhosted.org/Flask-Bootstrap/)
   ```shell
   pip install flask-bootstrap
   ```
 - _Flask-Moment_ : a small Flask extension that makes it very easy to incorporate moment.js into your application.
   ```shell
   pip install flask-moment
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
    - The `flask db migrate` command does not make any changes to the database, it just generates the migration script. To apply the changes to the database, the `flask db upgrade` command must be used.
    - The `upgrade()` function applies the migration, and the `downgrade()` function removes it.
    - Flask-SQLAlchemy uses a "snake case" naming convention for database tables by default. For the `User` model above, the corresponding table in the database will be named `user`. For a `AddressAndPhone` model class, the table would be named `address_and_phone`. If you prefer to choose your own table names, you can add an attribute named `__tablename__ `to the model class, set to the desired name as a string.
    - Because this application uses SQLite, the `upgrade` command will detect that a database does not exist and will create it (you will notice a file named _app.db_ is added after this command finishes, that is the SQLite database). When working with database servers such as MySQL and PostgreSQL, you have to create the database in the database server before running `upgrade`.
    - __Database Upgrade and Downgrade Workflow :__  With database migration support, after you modify the models in your application you generate a new migration script (`flask db migrate`), you probably review it to make sure the automatic generation did the right thing, and then apply the changes to your development database (`flask db upgrade`). You will add the migration script to source control and commit it.  
    When you are ready to release the new version of the application to your production server, all you need to do is grab the updated version of your application, which will include the new migration script, and run `flask db upgrade`. Alembic will detect that the production database is not updated to the latest revision of the schema, and run all the new migration scripts that were created after the previous release.  
    As I mentioned earlier, you also have a `flask db downgrade` command, which undoes the last migration. While you will be unlikely to need this option on a production system, you may find it very useful during development. You may have generated a migration script and applied it, only to find that the changes that you made are not exactly what you need. In this case, you can downgrade the database, delete the migration script, and then generate a new one to replace it.
    - In `User` model:
    ```
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    ```
    - In `Post` model:
    ```
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    ```

    - It is an unfortunate inconsistency that in some instances such as in a `db.relationship()` call, the model is referenced by the model class, which typically starts with an uppercase character, while in other cases such as this `db.ForeignKey()` declaration, a model is given by its database table name, for which SQLAlchemy automatically uses lowercase characters and, for multi-word model names, snake case.
    - For a one-to-many relationship, a `db.relationship` field is normally defined on the "one" side, and is used as a convenient way to get access to the "many".
    - The first argument to `db.relationship` is the model class that represents the "many" side of the relationship. This argument can be provided as a string with the class name if the model is defined later in the module. 
    - If you would want to have a one-to-one relationship you can pass `uselist=False` to `relationship()`.
    - The `backref` argument defines the name of a field that will be added to the objects of the "many" class that points back at the "one" object. This will add a `post.author` expression that will return the user given a post. 
    - The `lazy` argument defines how the database query for the relationship will be issued
    - `lazy` defines when SQLAlchemy will load the data from the database:

         - `'select'` / `True` (which is the default, but explicit is better than implicit) means that SQLAlchemy will load the data as necessary in one go using a standard select statement.
         - `'joined'` / `False` tells SQLAlchemy to load the relationship in the same query as the parent using a `JOIN` statement.
         - `'subquery'` works like `'joined'` but instead SQLAlchemy will use a subquery.
         - `'dynamic'` is special and can be useful if you have many items and always want to apply additional SQL filters to them. Instead of loading the items SQLAlchemy will return another query object which you can further refine before loading the items. Note that this cannot be turned into a different loading strategy when querying so it’s often a good idea to avoid using this in favor of `lazy=True`. A query object equivalent to a dynamic user.posts relationship can be created using `Post.query.with_parent(user)` while still being able to use lazy or eager loading on the relationship itself as necessary.
      - How do you define the lazy status for backrefs? By using the `backref()` function:
      ```
      posts = db.relationship('Post', backref=db.backref('author', lazy='joined'), lazy='dynamic')
      ```

    - Changes to a database are done in the context of a session, which can be accessed as `db.session`. Multiple changes can be accumulated in a session and once all the changes have been registered you can issue a single `db.session.commit()`, which writes all the changes atomically. If at any time while working on a session there is an error, a call to db.session.rollback() will abort the session and remove any changes stored in it.
    - All models have a `query` attribute that is the entry point to run database queries.
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
    - Because Flask-Login knows nothing about databases, it needs the application's help in loading a user. For that reason, the extension expects that the application will configure a user loader function, that can be called to load a user given the ID. This function can be added in the _app/models.py_ module:
      ```python
      @login.user_loader
      def load_user(id):
         return User.query.get(int(id))
      ```
    - `login_user()` function, which comes from Flask-Login, will register the user as logged in, so that means that any future pages the user navigates to will have the `current_user` variable set to that user.
    - Flask-Login's `logout_user()` function is used to log users out of the application.
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

 - [__Gravatar__](https://en.gravatar.com/) : To request an image for a given user, a URL with the format https://www.gravatar.com/avatar/[hash], where `[hash]` is the MD5 hash of the user's email address.  
   - Remember, MD5 support in Python works on bytes and not on strings.
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

- The representation of a many-to-many relationship requires the use of an auxiliary table called an _association table_. 
- __*self-referential relationship :*__ A relationship in which instances of a class are linked to other instances of the same class

- An auxiliary table that has no data other than the foreign keys is created without an associated model class.
   ```python
   followers = db.Table('followers',
      db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
      db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
   )
   ```

- Declare the many-to-many relationship in the users table:
   ```python
   class User(UserMixin, db.Model):
      # ...
      followed = db.relationship(
         'User', secondary=followers,
         primaryjoin=(followers.c.follower_id == id),
         secondaryjoin=(followers.c.followed_id == id),
         backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')
   ```
- The __"c"__ is an attribute of SQLAlchemy tables that are not defined as models. For these tables, the table columns are all exposed as sub-attributes of this __"c"__ attribute.
- It is always best to move the application logic away from view functions and into models or other auxiliary classes or modules, because it makes unit testing much easier.

- The `filter()` method is lower level, as it can include arbitrary filtering conditions, unlike `filter_by()` which can only check for equality to a constant value.

- __Query Terminators :__
   - `all()`
   - `first()`
   - `count()`

- __Unit Testing :__
   - `unittest` : Python package that makes it easy to write and execute unit tests.
   - The `setUp()` and `tearDown()` methods are special methods that the unit testing framework executes before and after each test respectively.
   - By changing the application configuration to `sqlite://` , SQLAlchemy uses an in-memory SQLite database during the tests.
   - The `db.create_all()` call creates all the database tables. This is a quick way to create a database from scratch that is useful for testing. 

- It is a standard practice to respond to a `POST` request generated by a web form submission with a redirect. This helps mitigate an annoyance with how the refresh command is implemented in web browsers. All the web browser does when you hit the refresh key is to re-issue the last request. If a `POST` request with a form submission returns a regular response, then a refresh will re-submit the form. Because this is unexpected, the browser is going to ask the user to confirm the duplicate submission, but most users will not understand what the browser is asking them. But if a `POST` request is answered with a redirect, the browser is now instructed to send a `GET` request to grab the page indicated in the redirect, so now the last request is not a `POST` request anymore, and the refresh command works in a more predictable way.

This simple trick is called the __Post/Redirect/Get__ pattern. It avoids inserting duplicate posts when a user inadvertently refreshes the page after submitting a web form.
- __[Post/Redirect/Get (PRG)](https://en.wikipedia.org/wiki/Post/Redirect/Get)__ pattern: A web development design pattern that prevents some duplicate form submissions, creating a more intuitive interface for user agents (users). PRG supports bookmarks and the refresh button in a predictable way that does not create duplicate form submissions.

- To prevent the _index.html_ template from crashing when it tries to render a web form that does not exist, add a conditional that only renders the form if it is defined.

- __Pagination :__ 
   - Flask-SQLAlchemy supports pagination natively with the `paginate()` query method.
      ```python
      user.followed_posts().paginate(1, 20, False).items
      ```
   - The `paginate` method can be called on any query object from Flask-SQLAlchemy. 
   - The return value from `paginate` is an object of a `Pagination` class from Flask-SQLAlchemy. The `items` attribute of this object contains the list of items in the requested page, alongwith other useful attributes that are useful when building pagination links:
      - `has_next`: True if there is at least one more page after the current one
      - `has_prev`: True if there is at least one more page before the current one
      - `next_num`: page number for the next page
      - `prev_num`: page number for the previous page

- __Email Support :__ 
   - Like most Flask extensions, you need to create an instance right after the Flask application is created.
      ```shell
      # ...
      from flask_mail import Mail

      app = Flask(__name__)
      # ...
      mail = Mail(app)
      ```
   
      ```shell
      from flask_mail import Message
      from app import mail

      def send_email(subject, sender, recipients, text_body, html_body):
         msg = Message(subject, sender=sender, recipients=recipients)
         msg.body = text_body
         msg.html = html_body
         mail.send(msg)
      ```

   - __How do JWTs work?__
      ```shell
      >>> import jwt
      >>> token = jwt.encode({'a': 'b'}, 'my-secret', algorithm='HS256')
      >>> token
      b'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhIjoiYiJ9.dvOo58OBDHiuSHD4uW88nfJikhYAXc_sfUHq1mDi4G0'
      >>> jwt.decode(token, 'my-secret', algorithms=['HS256'])
      {'a': 'b'}
      ```

      - The contents of the token, including the payload, can be decoded easily by anyone (Copy the above token and then enter it in the [JWT debugger](https://jwt.io/#debugger-io) to see its contents). What makes the token secure is that the payload is _signed_. If somebody tried to forge or tamper with the payload in a token, then the signature would be invalidated, and to generate a new signature the secret key is needed. When a token is verified, the contents of the payload are decoded and returned back to the caller. If the token's signature was validated, then the payload can be trusted as authentic.
      - The payload that I'm going to use for the password reset tokens is going to have the format `{'reset_password': user_id, 'exp': token_expiration}`. The `exp` field is standard for JWTs and if present it indicates an expiration time for the token. If a token has a valid signature, but it is past its expiration timestamp, then it will also be considered invalid.

      - Note that the `decode('utf-8')` is necessary because the `jwt.encode()` function returns the token as a byte sequence, but in the application it is more convenient to have the token as a string.

   - `@staticmethod` : A static method is similar to a class method, with the only difference that static methods do not receive the class as a first argument. A static method can be invoked directly from the class.

   - When `_external=True` is passed as an argument, complete URLs are generated

   - __Asynchronous Emails :__
      - Python has support for running asynchronous tasks, actually in more than one way. The `threading` and `multiprocessing` modules can both do this. Starting a background thread for email being sent is much less resource intensive than starting a brand new process, so I'm going to go with that approach:
         ```python 
         from threading import Thread
         # ...

         def send_async_email(app, msg):
            with app.app_context():
               mail.send(msg)


         def send_email(subject, sender, recipients, text_body, html_body):
            msg = Message(subject, sender=sender, recipients=recipients)
            msg.body = text_body
            msg.html = html_body
            Thread(target=send_async_email, args=(app, msg)).start()
         ```
      - When working with threads there is an important design aspect of Flask that needs to be kept in mind. Flask uses _contexts_ to avoid having to pass arguments across functions. There are two types of contexts, the _application context_ and the _request context_. In most cases, these contexts are automatically managed by the framework, but when the application starts custom threads, contexts for those threads may need to be manually created.
      - The reason many extensions need to know the application instance is because they have their configuration stored in the `app.config` object.
      - The application context that is created with the `with app.app_context()` call makes the application instance accessible via the `current_app` variable from Flask.

- __Rendering Bootstrap Forms :__
   - Instead of having to style the form fields one by one, Flask-Bootstrap comes with a macro that accepts a Flask-WTF form object as an argument and renders the complete form using Bootstrap styles.
      ```html
      {% extends "base.html" %}
      {% import 'bootstrap/wtf.html' as wtf %}

      {% block app_content %}
         <h1>Register</h1>
         <div class="row">
            <div class="col-md-4">
                  {{ wtf.quick_form(form) }}
            </div>
         </div>
      {% endblock %}
      ```
   - `wtf.quick_form()` macro in a single line of code renders the complete form, including support for display validation errors, and all styled as appropriate for the Bootstrap framework.

- __Dates and Times :__
   - Server must manage times that are consistent and independent of location.
   - UTC is the most used uniform timezone and is supported in the `datetime` class
   - While standardizing the timestamps to UTC makes a lot of sense from the server's perspective, this creates a usability problem for users.
   - While users can be asked to enter their timezone when they access the site for the first time, as part of their registration, it would be more efficient if you could just grab the timezone setting from their computers. There are actually two ways to take advantage of the timezone information available via JavaScript:
      - The _"old school"_ approach would be to have the web browser somehow send the timezone information to the server when the user first logs on to the application. This could be done with an Ajax call, or much more simply with a meta refresh tag. 
      - The _"new school"_ approach would be to not change a thing in the server, and let the conversion from UTC to local timezone happen in the client, using JavaScript.

         - The second option is advantageous as the browser has also access to the system locale configuration, which specifies things like AM/PM vs. 24 hour clock, DD/MM/YYYY vs. MM/DD/YYYY and many other cultural or regional styles. Addtionally, there is an open-source library that does all this work! (__Moment.js__)
   - __[Moment.js](https://momentjs.com/)__
      - a small open-source JavaScript library that takes date and time rendering to another level, as it provides every imaginable formatting option, and then some.
         ```python
         # ...
         from flask_moment import Moment

         app = Flask(__name__)
         # ...
         moment = Moment(app)
         ```

         ```python
         {% block scripts %}
            {{ super() }}
            {{ moment.include_moment() }}
         {% endblock %}
         ```
      - Moment.js makes a `moment` class available to the browser. The `moment` object provides several methods for different rendering options.
         ```shell
         moment('2017-09-28T21:45:23Z').format('L')
         "09/28/2017"
         moment('2017-09-28T21:45:23Z').format('LL')
         "September 28, 2017"
         moment('2017-09-28T21:45:23Z').format('LLL')
         "September 28, 2017 2:45 PM"
         moment('2017-09-28T21:45:23Z').format('LLLL')
         "Thursday, September 28, 2017 2:45 PM"
         moment('2017-09-28T21:45:23Z').format('dddd')
         "Thursday"
         moment('2017-09-28T21:45:23Z').fromNow()
         "7 hours ago"
         moment('2017-09-28T21:45:23Z').calendar()
         "Today at 2:45 PM"
         ```
      - The Flask-Moment extension greatly simplifies the use of moment.js by enabling a `moment` object similar to the JavaScript one in your templates.
         ```html
         {% if user.last_seen %}
         <p>Last seen on: {{ moment(user.last_seen).format('LLL') }}</p>
         {% endif %}
         ```

         ```html
         <a href="{{ url_for('user', username=post.author.username) }}">
            {{ post.author.username }}
         </a>
         said {{ moment(post.timestamp).fromNow() }}:
         <br>
         {{ post.body }}
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
