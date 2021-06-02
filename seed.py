from app import db
from models import Users, Posts

#clear and create our tables
db.drop_all()
db.create_all()

#create/add/commit user seed data
u1 = Users(first_name="Billy", last_name="Jenkins")
u2 = Users(first_name="Elisa", last_name="Sanchez Sanchez")
u3 = Users(first_name="Anton", last_name="Walker")
u4 = Users(first_name="Jose", last_name="Morales Diaz")
u5 = Users(first_name="Kate", last_name="Guimaraes")

#create/add/commit post seed data
p1 = Posts(title="Hi All", content="This is my first post", user_id=5)

db.session.add(u1)
db.session.add(u2)
db.session.add(u3)
db.session.add(u4)
db.session.add(u5)

db.session.add(p1)

db.session.commit()
