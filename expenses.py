# imports 
from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

#creates instance of this Class. 
# The first argument is the name of the application’s module or package.
# __name__ is a convenient shortcut for this that is appropriate for most cases. 
# This is needed so that Flask knows where to look for resources such as templates and static files.
app = Flask(__name__)
app.config["SECRET_KEY"] = "c4f86fdd81408bf0607e35b661f845a8"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    expenses = db.relationship("Expense", backref="user", lazy=True) # query which can pull all posts by one author
    
    def __repr__(self):
        return f'User("{self.username}", "{self.email}", "{self.id}")'
    

class Expense(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    amount = db.Column(db.Integer, index=True)
    description = db.Column(db.String, index=True)
    category = db.Column(db.String, index=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __repr__(self):
        return f'Expense("{self.userId}", "{self.amount}", "{self.category}")'
    

expenses = [
    {
        "id": 1,
        "amount": 25.50,
        "description": "Parking costs",
        "category": "Travel",
        "userId": 123
    },
    {
        "id": 2,
        "amount": 5.20,
        "description": "Lunch",
        "category": "Food",
        "userId": 123
    }
]

#the route() decorator to tell Flask what URL should trigger our function
@app.route("/")
@app.route("/home")
#function returns the message we want to display in the user’s browser. 
def home():
    return render_template("home.html", expenses=expenses)

@app.route("/update")
def update():
    form = RegistrationForm()
    if form.validate_on_submit():
        expense = Expense(amount=form.amount.data,
        description=form.description.data, category=form.category.data)
        db.session.update(expense)
        db.session.commit()
        flash(f"Expense updated", "success")
        return redirect(url_for("home"))
    return render_template("update.html", title="Update", form=form)


@app.route("/add", methods=["GET", "POST"])
def add_expense():
    form = RegistrationForm()
    if form.validate_on_submit():
        expense = Expense(amount=form.amount.data,
        description=form.description.data, category=form.category.data)
        db.session.add(expense)
        db.session.commit()
        flash(f"Expense added", "success")
        return redirect(url_for("home"))
    return render_template("add_expense.html", title="Add Expense", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "admin@blog.com" and form.password.data == "password":
            flash("You have been logged in!", "success")
            return redirect(url_for("home"))
        else:
            flash("Login unsuccessful. Please check username and password", "danger")
    return render_template("login.html", title="Log In", form=form)









with app.app_context():
    db.create_all()
# can use flask --app flaskblog.py run in the PC terminal to run it BUT....
# this allows it to run in debug mode, just type python flaskblog.py
if __name__ == '__main__':
    app.run(debug=True)