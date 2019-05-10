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
 ```shell
 pip install flask-wtf
 ```

 - The `form.hidden_tag()` template argument generates a hidden field that includes a token that is used to protect the form against CSRF attacks. All you need to do to have the form protected is include this hidden field and have the `SECRET_KEY` variable defined in the Flask configuration. If you take care of these two things, Flask-WTF does the rest for you.

 - The `flash()`, imported from Flask function is a useful way to show a message to the user.

 - This `redirect()` function instructs the client web browser to automatically navigate to a different page, given as an argument.

 - To have better control over links, Flask provides a function called `url_for()`, which generates URLs using its internal mapping of URLs to view functions. For example, `url_for('login')` returns `/login`, and `url_for('index')` return `/index`. The argument to `url_for()` is the endpoint name, which is the name of the view function.

 ## Resources :
 - [flask](https://github.com/pallets/flask): The Python micro framework for building web applications. https://www.palletsprojects.com/p/flask/
 - [The Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
 - [Flask-WTF](https://flask-wtf.readthedocs.io/en/stable/) : Simple integration of Flask and WTForms, including CSRF, file upload, and reCAPTCHA.
