from flask_app import app
from flask import render_template, redirect, session, flash, request
from flask_app.controllers import user_controller
from flask_app.models.form_model import Form



@app.route('/form')
def form_page():
    return render_template('form.html')

@app.route('/submit_form', methods=['POST'])
def form_submit():
    if 'user' not in session:
        if not Form.validate_form(request.form):
            return redirect('/form')
    if not Form.validate_form(request.form):
        return redirect('/home')
    data = {
        'name':request.form['name'],
        'email':request.form['email'],
        'church_name':request.form['church_name'],
        'church_address':request.form['church_address'],
        'description':request.form['description']
    }
    Form.send_form_via_email(data)
    if 'user' not in session:
        return redirect('/')
    return redirect('/home')