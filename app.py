from flask import Flask, render_template, request , redirect
from flask_sqlalchemy import SQLAlchemy
# from flask_mysqldb import MySQLdb
# from MYSQL import MySQLdb
from datetime import datetime


app = Flask(__name__)

# ------ERROR-----------------
# app.config['MYSQL_HOST']='localhost'
# app.config['MYSQL_USER']='root'
# app.config['MYSQL_PASSWORD']='root'
# app.config['MYSQL_DB']='todo'
# mysql=MYSQL(app)
# ---------------------------------

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db=SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer , primary_key=True)
    title = db.Column(db.String(200) , nullable=True)
    desc = db.Column(db.String(500) , nullable=True)
    date_created = db.Column(db.DateTime , default=datetime.utcnow)

    def __repr__(self):
        return f"{self.sno} - {self.title}"

@app.route('/', methods=['GET','POST'])
def hello_world():
    if request.method=='POST':
        # print("POST")
        # print(request.form['title'])
        title=request.form['title']
        desc=request.form['desc']  
        todo = Todo(title=title,desc=desc)
        db.session.add(todo)
        db.session.commit()
    allTodo = Todo.query.all()
    # print(allTodo)
    return render_template('index.html',allTodo=allTodo)
    # return 'Hello, World!'


@app.route('/products')
def products():
    return 'this is products page!'
    

@app.route('/show')
def show():
    allTodo = Todo.query.all()
    print(allTodo)
    return 'This is shoow page'

@app.route('/update/<int:sno>', methods=['GET','POST'])
def update(sno):
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']  
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title =title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
        
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html' , todo=todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

if __name__=="__main__":
    app.run(debug=True,port=8000) #While Development its show error
    # app.run(debug=False,port=8000) #After Development its show internal error to user
    
    # app.run(debug=True,port=8000) for changing port

