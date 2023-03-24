from flask import Flask, render_template, abort, session, url_for, redirect
from forms import LoginForm, SignUpForm, ModifyPet
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = 'dfewfew123213rwdsgert34tgfd1234trgf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///practice.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

"""object 'db' created of SQLAlchemy class"""
db = SQLAlchemy(app)


"""Table for Pets"""
class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    age = db.Column(db.String)
    bio = db.Column(db.String)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    form = ModifyPet()
    return render_template("insert_pet.html", form= form)


@app.route("/insert_pet", methods=["GET", "POST"])
def insert_pet():
    form = ModifyPet()
    if form.validate_on_submit():
        pet = Pet(name = form.name.data, age = form.age.data, bio = form.bio.data)
        db.session.add(pet)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
        finally:
            db.session.close()
    return render_template("insert_pet.html",  message="Insert Method found")


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
    return redirect(url_for('home', _scheme='https', _external=True))

if __name__ == '__main__':
    app.run(debug = True, port = 5000, host = "0.0.0.0")