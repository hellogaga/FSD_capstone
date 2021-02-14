from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

# local database setting
database_name = "dict"
username = 'postgres'
password = '123456'

# Heroku database
if 'DATABASE_URL' in os.environ:
  database_path = os.environ['DATABASE_URL']
else:
  database_path = "postgres://{}:{}@{}/{}".format(username,password,'127.0.0.1:5432', database_name)

# Initiate db
db = SQLAlchemy()

def setup_db(app, database_path=database_path):
  '''
  setup_db(app)
  binds a flask application and a SQLAlchemy service
  '''
  app.config["SQLALCHEMY_DATABASE_URI"] = database_path
  app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
  db.app = app
  db.init_app(app)
  db.create_all()

class Dictionary(db.Model):
  __tablename__ = 'Dictionary'

  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.String, nullable=False)
  # Define the question and answer
  swedishword = db.Column(db.String, nullable=False)
  meaninginenglish = db.Column(db.String)
  meaninginswedish = db.Column(db.String)
  note = db.Column(db.String(120),default='')
  # Foreign key value, user_id
  category_id = db.Column(db.Integer, db.ForeignKey('Categories.id'), nullable=False)
  # Back_ref
  answer_record = db.relationship('AnswerRecords', backref='Dictionary',lazy='dynamic') 

  def __init__(self, user_id, swedishword, category_id,
              meaninginenglish = None, 
              meaninginswedish = None,
              note = None):
    self.user_id = user_id
    self.swedishword = swedishword
    self.category_id = category_id
    self.meaninginenglish = meaninginenglish
    self.meaninginswedish = meaninginswedish
    self.note = note

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()
  
  def format(self):
    return{
      'id': self.id,
      'user_id': self.user_id,
      'swedishword': self.swedishword, 
      'category_id': self.category_id, 
      'meaninginenglish': self.meaninginenglish, 
      'meaninginswedish': self.meaninginswedish,
      'note': self.note 
    }

  def __repr__(self):
    return f'<Word {self.id} : {self.swedishword}>'

class Categories(db.Model):
  __tablename__ = 'Categories'
  id = db.Column(db.Integer, primary_key=True)
  category = db.Column(db.String, nullable=False)
  # Backref
  Dictionary = db.relationship('Dictionary', backref='Categories', lazy='dynamic')
  
  def __init__(self, category):
    self.category = category
  
  def insert(self):
      db.session.add(self)
      db.session.commit()
    
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()
  
  def format(self):
    return {
      'id':self.id,
      'category':self.category
    }

  def __repr__(self):
    return f'<Category {self.id} is: {self.category}>'
  

class AnswerRecords(db.Model):
  __tablename__ = 'AnswerRecords'
  id = db.Column(db.Integer, primary_key=True)
  time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  dict_id = db.Column(db.Integer, db.ForeignKey('Dictionary.id'), nullable=False)
  user_id = db.Column(db.String, nullable=False)
  result = db.Column(db.Boolean, nullable=False)

  def __init__(self, dict_id, user_id, result,
               time=None):
    self.dict_id = dict_id
    self.user_id = user_id
    self.result = result
    self.time = time
  
  def insert(self):
      db.session.add(self)
      db.session.commit()
    
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()
  
  def format(self):
    return{
      'Word_id':self.dict_id,
      'Time': self.time,
      'Answer_result': self.result
    }

  def __repr__(self):
      return f'<User {self.user_id}, Question {self.dict_id}, Result {self.result}>'




