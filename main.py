from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import mysql.connector, json
from datetime import datetime
 


local_server= True
with open ('config.json', 'r') as c:
    params= json.load(c)["parameters"]
app= Flask(__name__)


if (local_server):
    app.config["SQLALCHEMY_DATABASE_URI"] = params['local_uri'] # To make app configurable
else:
     app.config["SQLALCHEMY_DATABASE_URI"] = params['prod_uri'] 

# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:@localhost/codingthunder"
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://username:password@localhost/db_name"
db = SQLAlchemy(app)


class contact(db.Model): # contact is table name in database 
    # these variable my be diferent from database table column names.
    Sno = db.Column(db.Integer, primary_key=True) 
    Name = db.Column(db.String(100), unique=False, nullable=False) 
    Email = db.Column(db.String(132), nullable=False)
    phone = db.Column(db.String(60), nullable=False)
    mes = db.Column(db.String(100), nullable=False)
    datetime = db.Column(db.String(32), nullable=True)

class post(db.Model): # post is table name in database 
    # These variable my be diferent from database table column names.
    Sno = db.Column(db.Integer, primary_key=True) 
    title = db.Column(db.String(60), unique=False, nullable=False) 
    Slug = db.Column(db.String(25), nullable=False)
    Content = db.Column(db.String(100), nullable=False)
    Date = db.Column(db.String(6), nullable=True)
    # I do not know why Date variable should as same as in database table 
@app.route("/contact", methods= ['GET','POST'])
def Contact():
    if request.method=='POST':
        # variables specified in '' are being requested from html form's name property
        # PSK_name is just a variable it can be anything no need to be same as data base or html form
        PSK_name= request.form.get('name')  
        email= request.form.get('email')  
        phone= request.form.get('phone')
        message= request.form.get('message')
        entry= contact( Name = PSK_name, Email = email, phone = phone, mes = message, datetime= datetime.now() )
        db.session.add(entry) # LHS are model var and RHS are route var
        db.session.commit()
    return render_template('contact.html', data=params)



@app.route("/")
def home():
    posts= post.query.filter_by().all()
    return render_template('index.html', data=params, VAR=posts)

# @app.route("/dashbord")
# def dashbord():
#     return render_template('login.html', data=params)




@app.route("/about")
def about():
    return render_template('about.html', data=params)

@app.route("/post/<string:var>", methods=['GET'])
def post_route(var):
    P= post.query.filter_by(Slug=var).first()
    return render_template('post.html',data=params, POST=P)

if __name__ =="__main__":
    app.run(debug=True)