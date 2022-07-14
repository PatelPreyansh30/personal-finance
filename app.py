from flask import Flask, redirect,render_template,request
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from flask_security import *

app = Flask(__name__)

# DataBase Connectivity
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:@localhost/personal_finance_managment"
db = SQLAlchemy(app)

# Database Schema
class Signup(db.Model):
    sno = db.Column(db.Integer, primary_key=True,nullable=False)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(60), nullable=False)
    m_no = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(8), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    date = db.Column(db.Date, default=date.today(), nullable=True)
    
    def __repr__(self) -> str:
        return f"Record of: {self.email} & {self.name}"


@app.route("/",methods=['GET','POST'])
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
    return render_template("index.html")

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

@app.route("/login",methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        # print(email,password)

    return render_template("login.html")

@app.route("/signup",methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        m_no = request.form.get('m_no')
        gender = request.form.get('gender')
        password = request.form.get('password')
        # print(name,email,m_no,gender,password)

        entry = Signup(name=name,email=email,m_no=m_no,gender=gender,password=password)
        db.session.add(entry)
        db.session.commit()

    return render_template("signup.html")

@app.route("/forgot",methods=['GET','POST'])
def forgot():
    if request.method == 'POST':
        email = request.form.get('email')
        # print(email)
    return render_template("forgot.html")

if __name__ == "__main__":
    app.run(debug=True)