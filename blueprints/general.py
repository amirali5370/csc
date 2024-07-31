from flask import Blueprint, render_template

app = Blueprint("general" , __name__)


@app.route("/")
def main():
    return render_template('home.html')


@app.route("/about")
def about():
    return "about us"
