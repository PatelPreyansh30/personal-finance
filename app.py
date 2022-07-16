from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from flask_security import *
import json

# Config JSON file
with open('config.json','r') as c:
    params = json.load(c)['params']
local_server = True


app = Flask(__name__)

# DataBase Connectivity
if local_server:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

db = SQLAlchemy(app)

# Database Schema
class Register(db.Model):
    UserID = db.Column(db.Integer, nullable=False, primary_key=True)
    Name = db.Column(db.String(25), nullable=False)
    Email = db.Column(db.String(30), nullable=False)
    Mno = db.Column(db.String(15), nullable=False)
    Gender = db.Column(db.String(10), nullable=False)
    Password = db.Column(db.String(20), nullable=False)
    Date = db.Column(db.Date, default=date.today(), nullable=False)

    def __repr__(self) -> str:
        return f"Record of: {self.email} & {self.name}"


@app.route("/", methods=['GET', 'POST'])
def home():
    # if request.method == 'POST':
    #     if request.form.get('credit'):
    #         credit = request.form['credit']
    #         data = PFManage(credit=credit,debit=0)
    #         db.session.add(data)
    #         db.session.commit()
    #     elif request.form.get('debit'):
    #         debit = request.form['debit']
    #         data = PFManage(credit=0,debit=debit)
    #         db.session.add(data)
    #         db.session.commit()

    # allData = PFManage.query.all()
    return redirect("/login")

# @app.route("/delete/int:<srNo>")
# def delete(srNo):
#     data = PFManage.query.filter_by(srNo=srNo).first()
#     db.session.delete(data)
#     db.session.commit()
#     return redirect("/")

# @app.route("/delete")
# def deleteAll():
#     data = PFManage.query.all()
#     db.session.query(PFManage).delete()
#     db.session.commit()
#     return redirect("/")

# Login Page Logic
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            query = Register.query.filter_by(Email=email).first()
            if query.Password == password:
                return redirect("index.html")
            else:
                return f"<h3>Password is Invalid, Please Try Again </h3>"
        except:
            return f"<h3>Login through valid mail id </h3>"

    return render_template("login.html")


# Signup Page Logic
@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        m_no = request.form.get('m_no')
        gender = request.form.get('gender')
        password = request.form.get('password')

        entry = Register(Name=name, Email=email, Mno=m_no,Gender=gender, Password=password)
        db.session.add(entry)
        db.session.commit()

    return render_template("signup.html")


# Reset Page Logic
@app.route("/reset", methods=['GET', 'POST'])
def reset():
    if request.method == 'POST':
        email = request.form.get('email')

        try:
            query = Register.query.filter_by(Email=email).first()
            return query.Password
        except:
            return f"<h3>Please Enter Valid Email</h3>"

    return render_template("reset.html")

if __name__ == "__main__":
    app.run(debug=True, threaded=True)