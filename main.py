from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import csv
import smtplib
from flask_bootstrap import Bootstrap

my_email = "aumbattul1111@gmail.com"
password = "dbyppcbwyhiyuaci"
coffee_quotes = ["Coffee is a way of stealing time which should by rights belong to your older self.",
                 "No one can understand the truth until he drinks of coffee’s frothy goodness.",
                 "People say money can’t buy happiness. They Lie. Money buys Coffee, Coffee makes Me Happy!",
                 "Coffee is the best thing to douse the sunrise with.",
                 "Coffee should be black as Hell, strong as death, and sweet as love.",
                 "Science may never come up with a better office communication system than the coffee break.",
                 "The powers of a man’s mind are directly proportional to the quantity of coffee he drank.",
                 "Drink coffee! Do Stupid Things Faster with More Energy.",
                 "A cup of gourmet coffee shared with a friend is happiness tasted and time well spent.",
                 "It doesn’t matter where you’re from—or how you feel…there’s always peace in a strong cup of coffee.",
                 "Never underestimate the power of a good cup of coffee."]

app = Flask(__name__)
app.config['SECRET_KEY'] = 'This is a secret ky'

Bootstrap(app)

class SearchForm(FlaskForm):
    cafe_name = StringField(validators=[DataRequired()])
    search = SubmitField(validators=[DataRequired()])

class ReservationForm(FlaskForm):
    name = StringField(validators=[DataRequired()])
    cafe_name = StringField(validators=[DataRequired()])
    email = StringField(validators=[DataRequired()])
    date_time = StringField(validators=[DataRequired()])
    contact = StringField(validators=[DataRequired()])
    person = StringField(validators=[DataRequired()])
    book = SubmitField("Book Now")

@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)

@app.route('/', methods=["GET", "POST"])
def home():
    form = SearchForm()
    rv_from = ReservationForm()
    if form.validate_on_submit():
        cafes_ = []
        searched = form.cafe_name.data
        csv_file = csv.reader(open('cafes.csv'))
        for cafe in csv_file:
            if cafe[0] == searched.title() or cafe[5] == searched.lower():
                cafes_.append(cafe)
        return render_template('cafes.html', quotes=coffee_quotes, searched=searched, cafes=cafes_)
    if rv_from.validate_on_submit():
        cafe_name = rv_from.cafe_name.data
        name = rv_from.name.data
        date_time = rv_from.date_time.data
        contact = rv_from.contact.data
        persons = rv_from.person.data
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(
            from_addr=my_email,
            to_addrs=f"{cafe_name.replace(' ', '')}@email.com",
            msg=f"Subject:RESERVATION ALERT!\n\n"
                f"Name:{name}\n"
                f"Date and Time: {date_time}\n"
                f"Contact: {contact}\n"
                f"Number of people: {persons}"
        )
        return render_template('index.html', form=form, rv=rv_from)
    return render_template('index.html',form=form, rv=rv_from)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/resevation')
def reservation():
    rv_from = ReservationForm()
    if rv_from.validate_on_submit():
        cafe_name = rv_from.cafe_name.data
        name = rv_from.name.data
        date_time = rv_from.date_time.data
        contact = rv_from.contact.data
        persons = rv_from.person.data
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(
            from_addr=my_email,
            to_addrs=f"{cafe_name.replace(' ', '')}@email.com",
            msg=f"Subject:RESERVATION ALERT!\n\n"
                f"Name:{name}\n"
                f"Date and Time: {date_time}\n"
                f"Contact: {contact}\n"
                f"Number of people: {persons}"
        )
        return render_template('reservation.html', rv=rv_from)
    return render_template('reservation.html', rv=rv_from)
if __name__ == '__main__':
    app.run(debug=True)
