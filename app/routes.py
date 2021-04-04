import os
from uuid import uuid4
from app import app
from firebase import firebase
from flask import Flask, render_template, request,send_file,jsonify,flash,url_for,redirect
from werkzeug.utils import secure_filename
from app.forms import Form

firebase = firebase.FirebaseApplication('https://kiddopia-73f9e-default-rtdb.firebaseio.com/', None)


@app.route('/')
@app.route('/home')
def home():
  result = firebase.get('/Users', None)
  print("result",type(result),result)
  return render_template("home.html", places=result,form=Form(request.form))

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    form = Form(request.form)
    if request.method == 'POST' and form.validate():

      # will register fields called 'username' and 'email'.

        userdata = dict(request.form)
        print("userdata",type(userdata),userdata)
        name = userdata["name"]
        email = userdata["email"]
        f = request.files['file']

        primary_key = str(uuid4())
        uploads_dir = os.path.join(os.path.dirname(__file__),'uploads_dir')
        f.save(os.path.join(uploads_dir, secure_filename(primary_key)))
        new_data = {"name": name, "email": email,"attachment":f.filename,"primary_key":primary_key}
        print("new_data_submit",new_data)
        firebase.post('/Users',data=new_data)
        result = firebase.get('/Users', None)
        return render_template("home.html", places=result,form=Form(request.form))
    else:
      result = firebase.get('/Users', None)
      return render_template("home.html",places = result,error = form.errors,form=Form(request.form))




@app.route('/edit', methods=['GET', 'POST'])
def edit():
    form = Form(request.form)
    if request.method == 'POST' and form.validate():
        userdata = dict(request.form)
        print("edit data", type(userdata), userdata)
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
          print("new_edit_data",new_data)
          firebase.put(url='/Users',name=id,data=new_data)


        # print("post_result", type(result), result)
        result = firebase.get('/Users', None)
        return render_template("home.html", places=result,form=Form(request.form))
    else:
        result = firebase.get('/Users', None)
        return render_template("home.html", places=result, error=form.errors, form=Form(request.form))

@app.route('/delete', methods=['GET', 'POST'])
def delete():
  if request.method == 'POST' and len(dict(request.form)) > 0:
    userdata = dict(request.form)
    print("delete data", type(userdata), userdata)
    id = userdata["id"]
    firebase.delete(url="/Users",name=id)
    result = firebase.get('/Users', None)
    return render_template("home.html", places=result)
  else:
    return "Sorry, there was an error."

@app.route('/downloads/<path:id>', methods=['GET', 'POST'])
def downloads(id):
    print("helllo shubham")
    print(" download id",id)
    user = firebase.get('/Users',name=id)
    attachment_name = user['attachment']
    filename = user['primary_key']
    print("attachment",attachment_name)

    file_path = os.path.join(os.path.dirname(__file__), 'uploads_dir',filename)
    print("file_path",type(file_path),file_path)

    return send_file(file_path, as_attachment=True,attachment_filename=attachment_name)



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
