from enum import unique
import re
from flask import Flask,render_template,redirect,request,url_for,make_response
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///data.db'
db=SQLAlchemy(app)

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(255),unique=True)
    password=db.Column(db.String(255))
    email=db.Column(db.String(255),unique=True)
    fullname=db.Column(db.String(255))

class Teacher(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    teacherusername=db.Column(db.String(255),unique=True)
    teacherpassword=db.Column(db.String(255))
    teacheremail=db.Column(db.String(255),unique=True)
    teacherfullname=db.Column(db.String(255))
@app.route("/")
def index():
    return render_template('index.html')

# Student
@app.route('/login',methods = ['POST', 'GET'])
def login():
    users=User.query.all()
    if request.method=='POST':
        for user in users:
            if user.username==request.form['username']:
                if user.password==request.form['password']:
                    resp=make_response(render_template('profile.html',user=user))
                    resp.set_cookie('loginStatus',str(user.id))
                    return resp
                else:
                  return redirect(url_for('login'))  
    return render_template('login.html')

@app.route('/register',methods = ['POST', 'GET'])
def register():
    if request.method=='POST':
        user=User(
            username=request.form['username'],
            password=request.form['password'],
            email=request.form['email'],
            fullname=request.form['fullname']
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/profile/<id>',methods = ['POST', 'GET'])
def profile(id):
    loginStat=request.cookies.get('loginStatus')
    user=User.query.get(id)
    if loginStat==str(user.id):
        return render_template('profile.html',user=user)
    else:
        return redirect(url_for('login'))

@app.route('/logout',methods = ['POST', 'GET'])
def logout():
    resp=make_response(render_template('index.html'))
    resp.set_cookie('loginStatus','False')
    return resp

# Teacher
@app.route('/teacherlogin',methods = ['POST', 'GET'])
def teacherlogin():
    teachers=Teacher.query.all()
    if request.method=='POST':
        for teacher in teachers:
            if teacher.teacherusername==request.form['teacherusername']:
                if teacher.teacherpassword==request.form['teacherpassword']:
                    resp=make_response(render_template('teacherprofile.html',teacher=teacher))
                    resp.set_cookie('loginStatus',str(teacher.id))
                    return resp
                else:
                  return redirect(url_for('teacherlogin'))  
    return render_template('teacherlogin.html')

@app.route('/teacherregister',methods = ['POST', 'GET'])
def teacherregister():
    if request.method=='POST':
        teacher=Teacher(
            teacherusername=request.form['teacherusername'],
            teacherpassword=request.form['teacherpassword'],
            teacheremail=request.form['teacheremail'],
            teacherfullname=request.form['teacherfullname']
        )
        db.session.add(teacher)
        db.session.commit()
        return redirect(url_for('teacherlogin'))
    return render_template('teacherregister.html')

@app.route('/teacherprofile/<id>',methods = ['POST', 'GET'])
def teacherprofile(id):
    loginStat=request.cookies.get('loginStatus')
    teacher=Teacher.query.get(id)
    if loginStat==str(teacher.id):
        return render_template('teacherprofile.html',teacher=teacher)
    else:
        return redirect(url_for('teacherlogin'))

@app.route('/teacherlogout',methods = ['POST', 'GET'])
def teacherlogout():
    resp=make_response(render_template('index.html'))
    resp.set_cookie('loginStatus','False')
    return resp



db.create_all()
if __name__ == '__main__':
   app.run(debug = True)