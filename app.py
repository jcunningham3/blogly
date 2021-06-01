from flask import Flask, request, flash, render_template, session, redirect
from models import db, connect_db, Users

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

################################################################################
################################################################################

@app.route('/')
def homepage():
    return render_template('home.html')

@app.route('/users/list')
# Show all users in the system
def show_users():
    users = Users.query.all()
    return render_template('show_users.html', users=users)

@app.route('/users/profile/<int:user_id>')
# Show a user and their profile
def user_profile(user_id):
    user = Users.query.get_or_404(user_id)
    return render_template('user_profile.html', user=user)

@app.route('/users/add')
def add_a_user():
    return render_template('add_a_user.html')

@app.route('/create', methods=['POST'])
def create_a_user():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    img_url = request.form['img_url']
    new_user = Users(first_name=first_name, last_name=last_name)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/users/list')

@app.route('/edit/<int:user_id>', methods=['POST'])
def edit_user(user_id):
    user = Users.query.get_or_404(user_id)

    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.img_url = request.form['img_url']
    db.session.commit()
    return redirect(f'/users/profile/{user_id}')

@app.route('/user/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = Users.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users/list')
