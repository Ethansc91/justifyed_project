from flask_app import app
from flask import render_template, redirect, session, flash, request
from flask_app.models.user_model import User
from flask_app.models.comment_model import Comment
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def login_page():
    return render_template('login.html')



@app.route('/register_user')
def register_user_page():
    return render_template('registration.html')

@app.route('/register_user', methods=['POST'])
def register_user():
    if not User.registration_validation(request.form):
        return redirect('/register_user')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'fname': request.form['fname'],
        'lname': request.form['lname'],
        'email': request.form['email'],
        'password': pw_hash,
        'cpassword': request.form['cpassword'],
    }
    user = User.save_user_db(data)
    session['user'] = user
    return redirect('/home')

@app.route('/home')
def home_page():
    if 'user' not in session:
        return redirect('/')
    data = {
        'id': session['user']
    }
    return render_template('home.html',user=User.get_user_by_id(data), comments=Comment.get_comments_with_user())

@app.route('/login_user', methods=['POST'])
def login_user():
    if not User.login_validation(request.form):
        return redirect('/')
    data = {'email': request.form['email']}
    user_in_db = User.get_user_by_email(data)
    if not user_in_db:
        flash('Invalid Email/Password', 'login')
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('Invalid Email/Password', 'login')
        return redirect('/')
    session['user'] = user_in_db.id
    return redirect('/home')

@app.route('/group')
def group_page():
    data = {
        'id': session['user']
    }
    return render_template('group.html', user=User.get_user_by_id(data))

@app.route('/store')
def store_page():
    data = {
        'id': session['user']
    }
    return render_template('store.html', user=User.get_user_by_id(data))

@app.route('/schedule')
def schdule_page():
    data = {
        'id': session['user']
    }
    return render_template('schedule.html', user=User.get_user_by_id(data))

@app.route('/profile')
def profile_page():
    data = {
        'id': session['user']
    }
    return render_template('profile_settings.html', user=User.get_user_by_id(data))

@app.route('/update_user/<int:id>')
def update_user_page(id):
    data = {
        'id': id
    }
    return render_template('update_user.html', user=User.get_user_by_id(data))

@app.route('/update_user/<int:id>', methods=['POST'])
def update_user(id):
    if 'user' not in session:
        return redirect('/')
    data = {
        'fname': request.form['fname'],
        'lname': request.form['lname'],
        'email': request.form['email'],
        'description': request.form['description'],
        'id': id
    }
    User.update_user(data)
    return redirect('/profile')

@app.route('/update_users_description/<int:id>', methods=['POST'])
def update_users_description(id):
    data = {
        'description': request.form['description'],
        'id': id
    }
    User.update_users_description(data)
    return redirect('/profile')

@app.route('/logout')
def logout_user():
    session.clear()
    return redirect('/')