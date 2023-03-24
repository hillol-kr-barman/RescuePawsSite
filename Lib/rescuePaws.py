from flask import Flask, render_template, abort, session, url_for, redirect
from forms import LoginForm, SignUpForm, ModifyPet
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = 'dfewfew123213rwdsgert34tgfd1234trgf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///practice.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

"""object 'db' created of SQLAlchemy class"""
db = SQLAlchemy(app)

"""Model for Pets."""


class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.String)
    bio = db.Column(db.String)
    posted_by = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"From Repr{self.name}"


"""Model for Users."""


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)
    pets = db.relationship('Pet', backref='user')

    def __repr__(self):
        return f"From Repr{self.name}"


"""this following two lines needed to create and run all the database models"""

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    pets = Pet.query.all()
    user_login_status = False
    current_user_id = User.query.get(session['user'])

    if 'user' in session:
        user_login_status = True
        return render_template("index.html", pets=pets, user_login_status=user_login_status,
                               user=current_user_id)
    return render_template("index.html", pets=pets, user_login_status=user_login_status)


@app.route("/<user_name>/my_pets", methods=['GET'])
def user_posts(user_name):
    user = User.query.get(session['user'])
    pets = Pet.query.filter_by(posted_by=user.id)
    return render_template("user_posts.html", pets=pets, user=user)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/insert_pet", methods=["GET", "POST"])
def insert_pet():
    form = ModifyPet()
    if form.validate_on_submit():
        pet = Pet(name=form.name.data, age=form.age.data, bio=form.bio.data, posted_by=session['user'])
        db.session.add(pet)
        try:
            db.session.commit()
            return redirect(url_for('home', _scheme='http', _external=True))
        except Exception as e:
            db.session.rollback()
        finally:
            db.session.close()
    return render_template("insert_pet.html", form=form)


@app.route("/details/<int:pet_id>", methods=['POST', 'GET'])
def pet_details(pet_id):
    """View function for Showing Details of Each Pet."""
    form = ModifyPet()
    pet = Pet.query.get(pet_id)
    if pet is None:
        abort(404, description="No Pet was Found with the given ID")

    if form.validate_on_submit():
        pet.name = form.name.data
        pet.age = form.age.data
        pet.bio = form.bio.data

        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return render_template('details.html', message="A pet with this name already exists!")
    return render_template("details.html", pet=pet, form=form)


@app.route("/delete/<int:pet_id>")
def delete_pet(pet_id):
    pet = Pet.query.get(pet_id)
    if pet is None:
        abort(404, description="No Pet was Found with the given ID")
    db.session.delete(pet)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
    return redirect(url_for('home', _scheme='http', _external=True))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        """requested user is the user we are trying to fetch via email"""
        user = User.query.filter_by(email=form.email.data, password=form.password.data).first()
        if user is None:
            return render_template('login.html', form=form, message="Wrong Credentials. Try Again")
        session['user'] = user.id
        print("User ID : " + str(user.id) + ", and Name : " + user.name + " just logged in!")
        return render_template('login.html', user_login_status=True, message="Successfully Logged in !")
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    username = User.query.filter(User.id == session['user']).first()
    if 'user' in session:
        print("ID : " + str(session['user']) + " and User : " + username.name + " just logged out!")
        session.pop('user')
    return redirect(url_for('home', _scheme='http', _external=True))


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()
    if form.validate_on_submit():

        new_user = User(email=form.email.data, name=form.name.data, password=form.password.data)
        db.session.add(new_user)

        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return render_template('sign_up.html', form=form, message='This email already exists. Try logging in.')
        finally:
            db.session.close()
        print(User.query.all())
        return render_template("sign_up.html", message="You Have Successfully Signed Up!")

    return render_template("sign_up.html", form=form)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
