import os
from uuid import uuid4
from app import app
import itertools
import time
import json

from firebase import firebase
from flask import render_template, request,send_file
from werkzeug.utils import secure_filename
from app.forms import Form

firebase = firebase.FirebaseApplication(app.config['DB_URI'], None)

@app.route('/')
@app.route('/home')
def home():
    try:
        result = firebase.get('/Users', None)
        return render_template("home.html", places=result,form=Form(request.form))
    except Exception as e:
        raise e

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    try:
        form = Form(request.form)
        if request.method == 'POST' and form.validate():

          # will register fields called 'username' and 'email'.

            userdata = dict(request.form)
            name = userdata["name"]
            email = userdata["email"]
            f = request.files['file']

            primary_key = str(uuid4())
            uploads_dir = os.path.join(os.path.dirname(__file__),'uploads_dir')
            f.save(os.path.join(uploads_dir, secure_filename(primary_key)))
            new_data = {"name": name, "email": email,"attachment":f.filename,"primary_key":primary_key}
            firebase.post('/Users',data=new_data)
            result = firebase.get('/Users', None)
            return render_template("home.html", places=result,form=Form(request.form))
        else:
          result = firebase.get('/Users', None)
          return render_template("home.html",places = result,error = form.errors,form=Form(request.form))
    except Exception as e:
        raise e




@app.route('/edit', methods=['GET', 'POST'])
def edit():
    try:
        form = Form(request.form)
        if request.method == 'POST' and form.validate():
            userdata = dict(request.form)
            id = userdata["id"]
            name = userdata["name"]
            email = userdata["email"]
            f = request.files['file']

            if f.filename == '':
              edit_url = "/Users/" + str(id)
              firebase.put(url=edit_url, name='name', data=name)
              firebase.put(url=edit_url, name='email', data=email)
            else:
              primary_key = str(uuid4())
              uploads_dir = os.path.join(os.path.dirname(__file__), 'uploads_dir')
              f.save(os.path.join(uploads_dir, secure_filename(primary_key)))
              new_data = {"name": name, "email": email, "attachment": f.filename, "primary_key": primary_key}
              firebase.put(url='/Users',name=id,data=new_data)


            result = firebase.get('/Users', None)
            return render_template("home.html", places=result,form=Form(request.form))
        else:
            result = firebase.get('/Users', None)
            return render_template("home.html", places=result, error=form.errors, form=Form(request.form))
    except Exception as e:
        raise e

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    try:
        if request.method == 'POST' and len(dict(request.form)) > 0:
            userdata = dict(request.form)
            id = userdata["id"]
            firebase.delete(url="/Users",name=id)
            result = firebase.get('/Users', None)
            return render_template("home.html", places=result)
        else:
            return "Sorry, there was an error."
    except Exception as e:
        raise e

@app.route('/downloads/<path:id>', methods=['GET', 'POST'])
def downloads(id):
    try:
        user = firebase.get('/Users',name=id)
        attachment_name = user['attachment']
        filename = user['primary_key']

        file_path = os.path.join(os.path.dirname(__file__), 'uploads_dir',filename)

        return send_file(file_path, as_attachment=True,attachment_filename=attachment_name)
    except Exception as e:
        raise e



@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r
