from database import Base, engine, SessionLocal
from models import User,Post


Base.metadata.create_all(bind=engine)


session = SessionLocal()

# New_User:
new_user = User(name="Shivam", email="shivam@123.com")
session.add(new_user)
session.commit()
session.refresh(new_user)

# New_Post:
new_post=Post(title="My First Post!",content="Enjoying My Training",user_id=new_user.id)
session.add(new_post)
session.commit()
session.refresh(new_post)


# Read"----

users = session.query(User).all()
for user in users:
    print(f'User Id: {user.id},Username: {user.name},Email: {user.email}')


posts=session.query(Post).all()
for post in posts:
    print(post.title,post.content,post.author,post.user_id)

session.close()

#-
session = SessionLocal()

user = session.query(User).filter_by(name="Shivam").first()
if user:
    user.email = "shivamupdated@example.com"
    session.commit()
    print("User email updated!")

session.close()


#--

session = SessionLocal()

user = session.query(User).filter_by(name="Shivam").first()
if user:
    session.delete(user)
    session.commit()
    print("User deleted!")

session.close()

# Filtering, Ordering & Limiting Outputs--
from sqlalchemy import desc

session = SessionLocal()

# Filter with multiple conditions
results = session.query(Post).filter(Post.title.like("%Post%")).order_by(desc(Post.id)).limit(2).all()

for post in results:
    print(post.id, post.title,post.author)

session.close()


# Joins (Manual SQLALchemy Joins)--
from sqlalchemy.orm import joinedload

session = SessionLocal()

posts = session.query(Post).options(joinedload(Post.author)).all()

for post in posts:
    print(f"{post.title} — written by {post.author.name}")

session.close()



#-- Executing Raw SQL Queries--
from sqlalchemy import text
from database import engine

with engine.connect() as conn:
    result = conn.execute(text("SELECT name, email FROM users WHERE name=:name"), {"name": "Shivam"})
    for row in result:
        print(row)



#-- Commit and Rollback (Transactions)----
session = SessionLocal()
try:
    user = User(name="NewUser", email="newuser@example.com")
    session.add(user)
    session.commit()
except Exception as e:
    session.rollback()
    print("Error:", e)
finally:
    session.close()


#-- Full - Text - Search (FST):----

from sqlalchemy import func
from database import SessionLocal
from models import Post

session = SessionLocal()

keyword = "database"
query = session.query(Post).filter(
    func.to_tsvector('english', Post.title + ' ' + Post.content)
    .match(keyword)
)

for post in query:
    print(post.id, post.title)

session.close()



#-- One - to - Many:-
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)

    # Relationship (one user → many posts)
    posts = relationship("Post", back_populates="author", cascade="all, delete")

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    author = relationship("User", back_populates="posts")

user = User(name="Shiva", email="shiva@example.com")
post1 = Post(title="My First Post", content="Hello world!", author=user)
post2 = Post(title="Another Post", content="Learning ORM", author=user)

session.add(user)
session.commit()

print(user.posts)




# One- to- One:--
class Profile(Base):
    __tablename__ = "profiles"
    id = Column(Integer, primary_key=True)
    bio = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)

    user = relationship("User", back_populates="profile")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    profile = relationship("Profile", back_populates="user", uselist=False)


profile = Profile(bio="Backend Developer")
user = User(name="Shiva", profile=profile)
session.add(user)
session.commit()

print(user.profile.bio)
print(profile.user.name)


# Many- to- Many:--

from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

# Association table:-
student_course = Table(
    "student_course",
    Base.metadata,
    Column("student_id", Integer, ForeignKey("students.id")),
    Column("course_id", Integer, ForeignKey("courses.id"))
)

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    name = Column(String)

    courses = relationship("Course", secondary=student_course, back_populates="students")

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True)
    title = Column(String)

    students = relationship("Student", secondary=student_course, back_populates="courses")


python_course = Course(title="Python 101")
sql_course = Course(title="SQL Mastery")

shiva = Student(name="Shiva", courses=[python_course, sql_course])

session.add(shiva)
session.commit()

print(shiva.courses)   # [Course(Python 101), Course(SQL Mastery)]
print(sql_course.students)  # [Student(Shiva)]





# Error- Handling/ Exception Management:--

from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from models import User
from database import SessionLocal

session = SessionLocal()

try:
    new_user = User(name="Shivam", email="shivam@email.com")
    session.add(new_user)
    session.commit()
except IntegrityError as e:
    session.rollback()
    print("Duplicate or constraint error:", e)
except SQLAlchemyError as e:
    session.rollback()
    print("Database error:", e)
finally:
    session.close()



#  Recommended Way of Session Handling:---
from contextlib import contextmanager

@contextmanager
def get_db_session():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Database error: {e}")
        raise
    finally:
        session.close()

with get_db_session() as session:
    user = User(name="Arnav", email="arnav@email.com")
    session.add(user)

