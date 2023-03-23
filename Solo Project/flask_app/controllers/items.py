from flask_app import app
from flask import Flask, flash, render_template, redirect, request, session, url_for
from flask_app.models.item import Item
from flask_app.models.user import User
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'C:\\Users\\nickb\\Desktop\\Python\\Projects\\Solo Project\\flask_app\\static\\imgs'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#Dashboard to list all items
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    return render_template('dashboard.html',user=User.get_by_id(data), items=Item.get_all())

@app.route('/new_item')
def new_item():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    return render_template('new_item.html', user=User.get_by_id(data))

@app.route('/new_item/submit', methods=['POST'])
def submit_item():
    if 'user_id' not in session:
        redirect('/')
    if not Item.validate_item(request.form):
        return redirect('/new_item')
    if 'image_upload' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['image_upload']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.instance_path,app.config['UPLOAD_FOLDER'], filename))
    data = {
        'user_id': session['user_id'],
        'name': request.form['name'],
        'price': request.form['price'],
        'description': request.form['description'],
        'image_upload': filename,
        'num_of': request.form['num_of'],
    }
    Item.save(data)
    return redirect('/dashboard')

@app.route('/view_item/<int:id>')
def view_item(id):
    if 'user_id' not in session:
        redirect('/')
    data = {
        'id': session['user_id']
    }
    return render_template('view_item.html', user=User.get_by_id(data), item=Item.get_by_id({'id':id}))

@app.route('/edit_item/<int:id>')
def edit_items(id):
    if 'user_id' not in session:
        redirect('/login')
    data = {
        'id': session['user_id']
    }
    return render_template('edit_item.html', user=User.get_by_id(data), item=Item.get_by_id({'id':id}))

@app.route('/edit_item/<int:id>/submit', methods=['POST'])
def subedit_item(id):
    if 'user_id' not in session:
        redirect('/')
    if not Item.validate_item(request.form):
        return redirect(f'/edit/{id}')
    if 'image_upload' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['image_upload']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.instance_path,app.config['UPLOAD_FOLDER'], filename))
    data = {
        'id': id,
        'name': request.form['name'],
        'price': request.form['price'],
        'description': request.form['description'],
        'image_upload': filename,
        'num_of': request.form['num_of'],
    }
    Item.update(data)
    return redirect('/dashboard')

@app.route('/delete/<int:id>')
def delete(id):
    if 'user_id' not in session:
        redirect('/')
    Item.remove({'id': id})
    return redirect('/dashboard')

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


