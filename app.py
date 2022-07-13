from flask import Flask, redirect,render_template,request
from flask_sqlalchemy import SQLAlchemy
from datetime import date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///pf.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class PFManage(db.Model):
    srNo = db.Column(db.Integer,primary_key=True,nullable=False)
    date = db.Column(db.Date, default=date.today(), nullable=False)
    credit = db.Column(db.Integer, nullable=False)
    debit = db.Column(db.Integer, nullable=False)
    
    def __repr__(self) -> str:
        return f"Record: {self.date}"

@app.route("/",methods=['GET','POST'])
def home():
    if request.method == 'POST':
        if request.form.get('credit'):
            credit = request.form['credit']
            data = PFManage(credit=credit,debit=0)
            db.session.add(data)
            db.session.commit()
        elif request.form.get('debit'):
            debit = request.form['debit']
            data = PFManage(credit=0,debit=debit)
            db.session.add(data)
            db.session.commit()

    allData = PFManage.query.all()
    return render_template("index.html",allData = allData)

@app.route("/delete/int:<srNo>")
def delete(srNo):
    data = PFManage.query.filter_by(srNo=srNo).first()
    db.session.delete(data)
    db.session.commit()
    return redirect("/")

@app.route("/delete")
def deleteAll():
    data = PFManage.query.all()
    db.session.query(PFManage).delete()
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)