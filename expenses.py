# imports 
from flask import Flask, render_template, url_for, flash, redirect
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm, UpdateForm

#creates instance of this Class. 
# The first argument is the name of the application’s module or package.
# __name__ is a convenient shortcut for this that is appropriate for most cases. 
# This is needed so that Flask knows where to look for resources such as templates and static files.
app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config["SECRET_KEY"] = "c4f86fdd81408bf0607e35b661f845a8"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db = SQLAlchemy(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, index=True, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    expenses = db.relationship("Expense", backref="user", lazy=True) # query which can pull all posts by one author
    
    def __repr__(self):
        return f'User("{self.username}", "{self.email}", "{self.id}")'
    

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(60), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    _max_id = 0
    
    def __init__(self, amount, description, category, user_id):
        self.amount = amount
        self.description = description
        self.category = category
        self.user_id = user_id
        
    
    def __repr__(self):
        return f'Expense("{self.id}", "{self.amount}", "{self.category}"), {self.user_id}'
    

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


@app.route("/update", methods=["GET", "PUT", "DELETE", "POST"])
def update():
    form = UpdateForm()
    if form.validate_on_submit():
        expense = Expense.query.get(form.id.data)
        expense.amount = form.amount.data
        expense.description = form.description.data
        expense.category = form.category.data
        db.session.commit()
        flash(f"Expense updated", "success")
        return redirect(url_for("home"))
    return render_template("update.html", title="Update", form=form)


@app.route("/add", methods=["GET", "POST"])
def add_expense():
    form = RegistrationForm()
    if form.validate_on_submit():
        user_id = current_user.id
        expense = Expense(amount=form.amount.data, description=form.description.data, 
                          category=form.category.data, user_id=user_id)
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