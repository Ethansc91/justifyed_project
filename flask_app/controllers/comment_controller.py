from flask_app import app
from flask import render_template, redirect, session, flash, request
from flask_app.controllers import user_controller
from flask_app.models.user_model import User
from flask_app.models.comment_model import Comment


@app.route('/add_comment', methods=['POST'])
def add_comment():
    if not Comment.validate_comments(request.form):
        return redirect('/home')
    data = {
        'content': request.form['content'],
        'rating': request.form['rating'],
        'user': session['user']
    }
    Comment.save_comment_with_user(data)
    return redirect('/home')


@app.route('/delete_comment/<int:id>')
def delete_comment(id):
    Comment.delete_comment(id)
    return redirect('/home')