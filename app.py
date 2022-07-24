from flask import *
from flask_login import *
from flask_sqlalchemy import SQLAlchemy
from flask_security import *
from werkzeug.security import *
from datetime import date,timedelta
from alerts import EmailAlerts, CheckFunctions

# App Declaration
app = Flask(__name__)

# Flask Security Declaration
app.secret_key = ''

# Declare Session Time-Out
app.permanent_session_lifetime = timedelta(minutes=5)

# Flask Login Manager
login_manager = LoginManager()
login_manager.init_app(app)

# DataBase Connectivity with Development & Production Server (Use PostgreSQL Database in Local or Heroku)
env = 'dev'
if env == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = ""
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ""
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Table Schema (Register)
class Register(db.Model):
    __tablename__ = 'register'
    UserID = db.Column(db.Integer, nullable=False, primary_key=True)
    Name = db.Column(db.String(30), nullable=False)
    Email = db.Column(db.String(40), nullable=False,unique=True)
    Mno = db.Column(db.String(150), nullable=False,unique=True)
    Gender = db.Column(db.String(10), nullable=False)
    Age = db.Column(db.Integer, nullable=False)
    Password = db.Column(db.String(150), nullable=False)
    Date = db.Column(db.Date, default=date.today(), nullable=False)

    def __repr__(self) -> str:
        return f"Record of: {self.Email} & {self.Name}"

# Table Schema (User Activity)


# User Request For App
@app.route("/",methods=['GET','POST'])
def index():
    return render_template("welcome.html")

# Home Page (login required)
@app.route("/home")
@login_required
def home():
    if 'login_email' and 'login_password' in session:
        return render_template('home.html')
    else:
        return redirect("/login")

# Login Page Logic
@app.route("/login", methods=['POST','GET'])
@login_manager.user_loader
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        session['login_email']=email
        session['login_password'] = password
        
        try:
            if Register.query.filter_by(Email=email).first().Email:
                try:
                    if check_password_hash(Register.query.filter_by(Email=email).first().Password,password):
                        return redirect("/home")
                    else:
                        raise Exception
                except:
                    return render_template("/authentication/login.html",valid_pass="Please enter valid password")
            else:
                raise Exception
        except:
            return render_template("/authentication/login.html",valid_email="Please enter valid email")

    return render_template("/authentication/login.html")

# Signup Page Logic
@app.route("/signup", methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        m_no = request.form.get('m_no')
        gender = request.form.get('gender')
        age = request.form.get('age')
        password = generate_password_hash(request.form.get('password'))

        email_ls = Register.query.with_entities(Register.Email).all()
        mno_ls = Register.query.with_entities(Register.Mno).all()
        
        if CheckFunctions.email_check(email_ls,email)==0:
            return render_template("/authentication/signup.html",email_check="Email is already registered")
        elif CheckFunctions.mno_check(mno_ls,m_no)==0:
            return render_template("/authentication/signup.html",mno_check="Mobile Number is already registered")
        else:
            entry = Register(Name=name, Email=email, Mno=m_no,Gender=gender,Age=age, Password=password)
            db.session.add(entry)
            db.session.commit()
            return render_template("/authentication/signup.html",signupmsg='True')
    
    return render_template("/authentication/signup.html")

# Reset Page Logic
@app.route("/reset", methods=['POST','GET'])
def reset():
    if request.method == 'POST':
        session['reset_email'] = request.form.get('email')
        try:
            Register.query.filter_by(Email=session['reset_email']).first().Email
            session['otp'] = EmailAlerts.email_otp(session['reset_email'])
            return render_template("/authentication/reset_otp.html",valid_email="Successfully sent the OTP on your email, if you don't recive OTP then check your email's spam folder")
        except:
            return render_template("/authentication/reset.html",invalid_email="Please enter valid email")

    return render_template("/authentication/reset.html")

# OTP Verify
@app.route("/verify",methods=["POST",'GET'])
def otp():
    if "reset_email" and "otp" in session:
        if request.method == "POST":
            OTP = request.form.get('otp')
            if str(session['otp']) == OTP:
                session.pop('otp',None)
                return render_template("/authentication/new_password.html")
            else:
                return render_template("/authentication/reset.html",invalid_otp="Your OTP is incorrect")
    else:
        return redirect("/")

# Reset The Password
@app.route("/set-password",methods=['POST','GET'])
def set_password():
    if "reset_email" in session:
        if request.method=='POST':
            newPass = generate_password_hash(request.form.get('new-password'))
            old_data = Register.query.filter_by(Email=session['reset_email']).first()
            old_data.Password = newPass
            db.session.commit()
            session.clear()
            return render_template("/authentication/new_password.html",reset_password_done="True")
        else:
            session.clear()
            return redirect('/login')
    else:
        return redirect("/")

# Running the App
if __name__ == "__main__":
    app.run()
