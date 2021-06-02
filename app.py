from flask import Flask, request, flash, render_template, session, redirect
from models import db, connect_db, Users, Posts

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'crowBottom'

connect_db(app)

################################################################################
################################################################################

@app.route('/')
def homepage():
    # show posts from users
    posts = Posts.query.limit(5).all()
    users = Users.query.all()
    return render_template('home.html', posts=posts, users=users)

# USER ROUTES ##################################################################

@app.route('/users/list')
# Show all users in the system
def show_users():
    users = Users.query.all()
    return render_template('show_users.html', users=users)

@app.route('/users/profile/<int:id>')
# Show a user and their profile
def user_profile(id):
    user = Users.query.get_or_404(id)
    posts = Posts.query.all()
    return render_template('user_profile.html', user=user, posts=posts)

@app.route('/users/add')
# add a new user form
def add_a_user():
    return render_template('add_a_user.html')

@app.route('/create', methods=['POST'])
# post the new user
def create_a_user():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    img_url = request.form['img_url']
    new_user = Users(first_name=first_name, last_name=last_name)
    db.session.add(new_user)
    db.session.commit()
    flash(f"Added {first_name} {last_name}!")
    return redirect('/users/list')

@app.route('/edit/<int:user_id>', methods=['POST'])
# edit a user and post it
def edit_user(user_id):
    user = Users.query.get_or_404(user_id)

    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.img_url = request.form['img_url']
    db.session.commit()
    flash(f"Edited {user.first_name} {user.last_name}!")
    return redirect(f'/users/profile/{user_id}')

@app.route('/user/delete/<int:user_id>', methods=['POST'])
# delete a user and post it
def delete_user(user_id):
    user = Users.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f"Deleted {user.first_name} {user.last_name}!")
    return redirect('/users/list')

# USER POSTS ROUTES ##################################################################

@app.route('/post/create/<int:user_id>', methods=["POST"])
# create a new post
def create_a_post(user_id):
    title = request.form['title']
    content = request.form['content']
    new_post = Posts(title=title, content=content, user_id=user_id)
    db.session.add(new_post)
    db.session.commit()
    flash("Post added!")
    return redirect(f'/users/profile/{user_id}')

@app.route('/post/view/<int:post_id>')
def view_a_post(post_id):
    post = Posts.query.get_or_404(post_id)
    return render_template('view_post.html', post=post)

@app.route('/edit/post/<int:post_id>', methods=['POST'])
# edit a user and post it
def edit_post(post_id):
    post = Posts.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    db.session.commit()
    flash(f"Edited {post.title}")
    return redirect(f'/post/view/{post.id}')

@app.route('/delete/post/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    post = Posts.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash(f'{post.title} post deleted!')
    return redirect(f'/users/profile/{post.user_id}')
