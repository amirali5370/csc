from flask import Blueprint, render_template


app = Blueprint("user" , __name__)


@app.route("/user")
def user():
    return "This is user page"