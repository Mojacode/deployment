from flask import render_template, request, redirect, session, flash
from flask_app import app
# from ..models.car import Car
from flask_app.models.user import User
from flask_app.models.tree import Tree
from flask_bcrypt import Bcrypt  
bcrypt = Bcrypt(app)  




# HTML ROUTING
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register/')
def registerPage():
    return render_template ('registration.html')

@app.route('/dashboard')
def dashboardPage():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'users_id' : session['user_id']
    }
    return render_template('dashboard.html', user = User.get_id(data), trees = Tree.get_all(data))




# REGISTRATION ROUTE
@app.route('/registered', methods = ['POST'])
def register():
    if not User.validate_register(request.form):
        return redirect('/register/')
    pw_hash= bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)

    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash
        }
    user_id = User.save(data)
    session['id'] = user_id
    return redirect('/')

# LOGGING IN ROUTE
@app.route('/login', methods = ['POST'])
def login():
    user= User.validate_email(request.form)
    if not user:
        flash("Email Not Found")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard')
    

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')