from flask import Blueprint, render_template, request, flash, redirect, session, abort
from models.teacher import Teacher
from models.quizzes import Quiz
from models.k_class import Class
from models.activates import Activate
from models.lessons import Lesson
from models.activates import Activate
from models.user import User
from flask_login import login_user
from extentions import db
from functuions.defs import get_classes,get_quizzes_with_class

app = Blueprint("teacher" , __name__)

current_teacher = ""

@app.before_request
def before_request():
        if session.get("teacher_login", None) == None and request.endpoint != "teacher.login":
            abort(403)
        elif request.endpoint == "teacher.login":
            pass
        else:
            global current_teacher
            id = session["teacher_login"]
            current_teacher = Teacher.query.filter(Teacher.id==id).first()




@app.route("/teacher/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        teacher = Teacher.query.filter(Teacher.username == username).first()

        if teacher == None:
            flash("نام کاربری یا رمز عبور اشتباه است")
            return redirect("/teacher/login")
        elif password == teacher.password :
            session["teacher_login"] = str(teacher.id)
            return redirect("/teacher/dashboard")
        else:
            flash("نام کاربری یا رمز عبور اشتباه است")
            return redirect("/teacher/login")
    else:
        return render_template("teacher/login.html")
    

@app.route("/teacher/dashboard")
def dashboard():
    return render_template("teacher/dashboard.html", teacher=current_teacher)


##############################   QUIZ   ###############################
@app.route("/teacher/dashboard/quizzes", methods=["GET","POST"])
def quizzes():
    if request.method == "POST":
        name = request.form.get("name")
        teacher_id = current_teacher.id
        teacher_name = current_teacher.firstName + " " + current_teacher.lastName

        q = Quiz(name = name, teacher_id=teacher_id, teacher_name=teacher_name)

        db.session.add(q)
        db.session.commit()
        return render_template("sucs.html", name=name, hidden="add", tHidden="qui")
    else:
        quizzes = current_teacher.quizzes.all()
        return render_template("teacher/quizzes.html", quizzes=quizzes, teacher=current_teacher)


@app.route("/teacher/dashboard/edit-quiz/<id>", methods=["GET","POST"])
def edit_quiz(id):
    quiz = Quiz.query.filter(Quiz.id==id).first_or_404()
    if request.method == "POST":
        name = request.form.get("name")

        quiz.name = name

        db.session.commit()
        
        return render_template("sucs.html", name=name, hidden="edit", tHidden="qui")
    else:
        return render_template("teacher/edit_quiz.html", quiz=quiz, teacher=current_teacher)
    

@app.route("/teacher/dashboard/delete-quiz/<id>")
def delete_quiz(id):
    quiz = Quiz.query.filter(Quiz.id==id).first_or_404()


    db.session.delete(quiz)
    db.session.commit()
        
    return redirect("/teacher/dashboard/quizzes")


@app.route("/teacher/dashboard/quizzes/<id>", methods = ["GET", "POST"])
def show_quiz(id):
    quiz = Quiz.query.filter(Quiz.id == id).first_or_404()
    activates = quiz.activates.all()
    if request.method == "POST":

        class_id = request.form.get("k_class", None)
        replace = Activate.query.filter(Activate.class_id==class_id).first()
        if replace != None and replace in activates:
            # TODO: مسیج باکس کلاس تکراری اجرا شود
            return redirect("/teacher/dashboard/quizzes/"+str(id))
        k_class = Class.query.filter(Class.id==class_id).first_or_404()
        class_name = k_class.grade + " " + k_class.name + " " + k_class.field

        a = Activate(quiz_id=quiz.id, class_id=class_id, class_name=class_name)

        db.session.add(a)
        db.session.commit()

        return redirect("/teacher/dashboard/quizzes/"+str(id))
    else:
        get_req = request.args.get("del", None)
        if get_req != None:
            object = Activate.query.filter(Activate.id == int(get_req)).first()
            db.session.delete(object)
            db.session.commit()
            return redirect("/teacher/dashboard/quizzes/"+str(id))
        else:
            classes = get_classes(current_teacher)
            return render_template("teacher/show_quiz.html", classes=classes, activates=activates, teacher=current_teacher, quiz=quiz)


##############################   CLASS   ###############################
@app.route("/teacher/dashboard/classes")
def classes():
        lessone = Lesson.query.filter(Lesson.teacher_id==current_teacher.id).order_by(Lesson.name).all()
        return render_template("teacher/classes.html", lessone=lessone, teacher=current_teacher)


@app.route("/teacher/dashboard/classes/<id>")
def show_class(id):
    this_class = Class.query.filter(Class.id==id).first_or_404()
    students = this_class.users.order_by(User.number).all()
    quizzes = get_quizzes_with_class(this_class)
    lessons = this_class.lessons.order_by(Lesson.name).all()

    return render_template("teacher/show_class.html", quizzes=quizzes, students=students, lessons=lessons, teacher=current_teacher, classes=this_class)
