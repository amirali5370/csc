from flask import Blueprint, json, render_template, request, session, redirect, abort, flash, url_for
import config
from models.k_class import Class
from models.user import User
from models.teacher import Teacher
from models.lessons import Lesson
from extentions import db

app = Blueprint("admin" , __name__)

@app.before_request
def before_request():
        if session.get("admin_login", None) == None and request.endpoint != "admin.login":
            abort(403)


##############################   ADMIN   ###############################
@app.route("/admin/login", methods = ["POST","GET"])
def login():
    if request.method == "POST":
        username = request.form.get('username',None)
        password = request.form.get('password',None)

        if username == config.ADMIN_USERNAME and password == config.ADMIN_PASSWORD:
            session["admin_login"] = username
            return redirect("/admin/dashboard")
        else:
            return redirect("/admin/login")
    else:
        return render_template("admin/login.html")


@app.route("/admin/dashboard", methods = ["GET"])
def dashboard():
    return render_template("admin/dashboard.html")


##############################   CLASS   ###############################
@app.route("/admin/dashboard/classes", methods = ["GET", "POST"])
def classes():
    if request.method == "POST":
        grade = request.form.get("grade", None)
        field = request.form.get("field", None)
        name = request.form.get("name", None)

        c = Class(grade=grade, field=field, name=name)

        db.session.add(c)
        db.session.commit()

        return render_template("sucs.html", name=name, grade=grade, field=field, hidden="add" ,tHidden="class")
    else:
        classes = Class.query.all()
        if request.args.get("h", None)=="d":
            return render_template("admin/classes.html", classes=classes, hidden="del")
        else:
            return render_template("admin/classes.html" , classes=classes)
    

@app.route("/admin/dashboard/edit-class/<id>", methods = ["GET", "POST"])
def edit_class(id):
    classes = Class.query.filter(Class.id == id).first_or_404()
    if request.method == "POST":
        grade = request.form.get("grade", None)
        field = request.form.get("field", None)
        name = request.form.get("name", None)
        if grade != classes.grade or field != classes.field or name != classes.name :
            users = classes.users.all()
            activates = classes.activates.all()
            lessons = classes.lessons.all()
            for u in users:
                u.grade = grade
                u.field = field
                u.class_name = name
            for a in activates:
                a.class_name = grade + " " + name + " " + field
            for l in lessons:
                l.class_name = grade + " " + name + " " + field

        classes.grade = grade
        classes.field = field
        classes.name = name

        db.session.commit()

        return render_template("sucs.html", name=name, grade=grade, field=field, hidden="edit" ,tHidden="class")
    else:
        return render_template("admin/edit_class.html", classes=classes)


@app.route("/admin/dashboard/del-class/<id>", methods = ["GET"])
def delete_class(id):
        status = request.args.get("status")
        if status == "true":
            classes = Class.query.filter(Class.id == id).first_or_404()
            db.session.delete(classes)
            db.session.commit()
        return redirect(url_for("admin.classes"))


@app.route("/admin/dashboard/classes/<id>", methods = ["GET", "POST"])
def lessons_of_class(id):
    this_class = Class.query.filter(Class.id == id).first_or_404()
    teachers = Teacher.query.all()

    if request.method == "POST":

        name = request.form.get("name", None)

        replace = Lesson.query.filter(Lesson.name==name).first()
        if replace != None:
            # TODO: مسیج باکس نام درس تکراری اجرا شود
            return redirect("/admin/dashboard/classes/"+str(id))
        

        teacher_id = request.form.get("teacher", None)
        class_id = this_class.id
        class_name = (this_class.grade + " " + this_class.name + " " + this_class.field)
        teacher = Teacher.query.filter(Teacher.id == teacher_id).first()
        teacher_name = ( teacher.firstName +" "+ teacher.lastName)



        l = Lesson(name=name, class_name=class_name, class_id=class_id, teacher_id=teacher_id, teacher=teacher_name)

        db.session.add(l)
        db.session.commit()

        return redirect("/admin/dashboard/classes/"+str(id))
    else:
        get_req = request.args.get("del", None)
        if get_req != None:
            object = Lesson.query.filter(Lesson.id == int(get_req)).first()
            db.session.delete(object)
            db.session.commit()
            return redirect("/admin/dashboard/classes/"+str(id))
        else:
            lessons = this_class.lessons.all()
            students = this_class.users.order_by(User.number).all()
            return render_template("admin/lesson_class.html", classes=this_class, teachers=teachers, lessons=lessons, students=students)
        

##############################   STUDENT   ###############################
@app.route("/admin/dashboard/students", methods = ["GET", "POST"])
def sutdents():
    if request.method == "POST":
        firstName = request.form.get("firstName", None)
        lastName = request.form.get("lastName", None)
        password = request.form.get("password", None)
        code = request.form.get("code", None)
        id_class = request.form.get("k_class", None)
        number = request.form.get("number", None)

        k_class = Class.query.filter(Class.id==id_class).first_or_404()

        u = User(firstName = firstName, lastName = lastName, username = code, password = password, code = code, grade = k_class.grade, field = k_class.field, class_name = k_class.name,  class_id = id_class, number = number)
        
        db.session.add(u)
        db.session.commit()

        return render_template("sucs.html", firstName=firstName, lastName=lastName, hidden="add", tHidden="stu")
    else:
        classes = Class.query.all()
        users = User.query.all()

        return render_template("admin/students.html", classes=classes, users=users)
    

@app.route("/admin/dashboard/edit-students/<id>", methods = ["GET", "POST"])
def edit_user(id):
    user = User.query.filter(User.id == id).first_or_404()
    if request.method == "POST":
        firstName = request.form.get("firstName", None)
        lastName = request.form.get("lastName", None)
        username = request.form.get("username", None)
        password = request.form.get("password", None)
        code = request.form.get("code", None)
        id_class = request.form.get("k_class", None)
        number = request.form.get("number", None)

        k_class = Class.query.filter(Class.id==id_class).first_or_404()

        user.firstName = firstName
        user.lastName = lastName
        user.username = username
        user.password = password
        user.code = code
        user.class_id = id_class
        user.number = number

        user.grade = k_class.grade
        user.field = k_class.field
        user.class_name	= k_class.name

        db.session.commit()

        return render_template("sucs.html", firstName=firstName, lastName=lastName, hidden="edit" ,tHidden="stu")
    else:
        classes = Class.query.all()
        return render_template("admin/edit_user.html", classes=classes , user=user)
    

@app.route("/admin/dashboard/del-students/<id>", methods = ["GET", "POST"])
def delete_user(id):
    user = User.query.filter(User.id == id).first_or_404()
    
    db.session.delete(user)
    db.session.commit()

    return redirect("/admin/dashboard/students")


##############################   TEACHER   ###############################
@app.route("/admin/dashboard/teachers", methods = ["GET", "POST"])
def teachers():
    if request.method == "POST":
        firstName = request.form.get("firstName", None)
        lastName = request.form.get("lastName", None)
        username = request.form.get("username", None)
        password = request.form.get("password", None)

        t = Teacher(firstName = firstName, lastName = lastName, username = username, password = password)
        
        db.session.add(t)
        db.session.commit()

        return render_template("sucs.html", firstName=firstName, lastName=lastName, hidden="add", tHidden="tea")
    else:
        teachers = Teacher.query.all()
        if request.args.get("h", None)=="d":
            return render_template("admin/teachers.html", teachers=teachers, hidden="del")
        else:
            return render_template("admin/teachers.html" , teachers=teachers)
    

@app.route("/admin/dashboard/edit-teacher/<id>", methods = ["GET", "POST"])
def edit_teacher(id):
    teacher = Teacher.query.filter(Teacher.id == id).first_or_404()
    if request.method == "POST":
        firstName = request.form.get("firstName", None)
        lastName = request.form.get("lastName", None)
        username = request.form.get("username", None)
        password = request.form.get("password", None)

        if firstName != teacher.firstName or lastName != teacher.lastName:
            qui = teacher.quizzes.all()
            les = teacher.lessons.all()
            for l in les:
                l.teacher = firstName + " " + lastName
            for q in qui:
                q.teacher_name = firstName + " " + lastName


        teacher.firstName = firstName
        teacher.lastName = lastName
        teacher.username = username
        teacher.password = password

        db.session.commit()

        return render_template("sucs.html", firstName=firstName, lastName=lastName, username=username, password=password, hidden="edit" ,tHidden="tea")
    else:
        return render_template("admin/edit_teacher.html", teacher=teacher)
    

@app.route("/admin/dashboard/del-teacher/<id>", methods = ["GET"])
def delete_teacher(id):
    teacher = Teacher.query.filter(Teacher.id == id).first_or_404()
    check_lessoneForTeacher = teacher.lessons.first()
    if check_lessoneForTeacher == None:
        db.session.delete(teacher)
        db.session.commit()
        return redirect("/admin/dashboard/teachers")
    else:
        return redirect("/admin/dashboard/teachers?h=d")
