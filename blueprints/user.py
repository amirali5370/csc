from flask import Blueprint, render_template
from models.k_class import Class
from models.quizzes import Quiz
from functuions.defs import get_quizzes_with_user

app = Blueprint("user" , __name__)


@app.route("/user")
def user():
    return "This is user page"