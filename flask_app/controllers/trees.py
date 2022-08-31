from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.tree import Tree
from flask_app.models.user import User

# ROUTE PAGES
@app.route('/show/tree/<int:tree_id>')
def show_tree(tree_id):
    if 'user_id' not in session:
        return redirect ('/')
    data={
        'id': tree_id,
        "users_id": session['user_id']
    }
    return render_template('showTree.html', user=User.get_id(data), trees = Tree.get_one(data))


@app.route('/newTree')
def newTreePage():
    if 'user_id' not in session:
        return redirect ('/')
    data={
        "users_id": session['user_id']
    }
    return render_template('newTree.html', user=User.get_id(data))

@app.route('/mytrees')
def myTreesPage():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'users_id' : session['user_id']
    }
    return render_template('myTrees.html', user = User.get_id(data), trees = Tree.get_all_from_user(data))

@app.route('/editTree/<int:tree_id>')
def editTreePage(tree_id):
    if 'user_id' not in session:
        return redirect ('/')
    data={
        'id': tree_id,
        "users_id": session['user_id']
    }
    return render_template('editTree.html', user=User.get_id(data), trees = Tree.get_one(data))

@app.route("/editTree/Edited", methods=["POST"])
def update_tree():
    
    if 'user_id' not in session:
        return redirect ('/')

    data={
        "species": request.form['species'],
        "location": request.form['location'],
        "reason": request.form['reason'],
        "dateplanted" : request.form['dateplanted'],
        "id": request.form['id']
    }
    Tree.update_tree(data)
    return redirect('/dashboard')


@app.route("/updateVisitor", methods=["POST"])
def update_visitor():
    
    if 'user_id' not in session:
        return redirect ('/')

    data={
        "visitor": request.form['visitors'],
        "id": request.form['id'],
        "users_id": session['user_id']
    }
    Tree.update_visitors(data)
    return redirect('/dashboard')


@app.route("/addTree", methods=["POST"])
def add_tree():
    if 'user_id' not in session:
        return redirect ('/')

    data={
        "species": request.form['species'],
        "location": request.form['location'],
        "reason": request.form['reason'],
        "dateplanted" : request.form['dateplanted'],
        "users_id": session['user_id']
    }
    Tree.save_tree(data)
    return redirect('/dashboard')

@app.route('/delete/<int:id>')
def delete(id):

    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id": id
    }
    Tree.delete(data)
    return redirect('/dashboard')