from flask import Flask
from flask_wtf.csrf import CSRFProtect
from blueprints.general import app as general
from blueprints.admin import app as admin
from blueprints.user import app as user
from blueprints.teacher import app as teacher
import config
import extentions
from flask_login import LoginManager
from models.teacher import Teacher

app = Flask(__name__)
app.register_blueprint(general)
app.register_blueprint(admin)
app.register_blueprint(user)
app.register_blueprint(teacher)


app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
app.config["SECRET_KEY"] = config.SECRET_KEY
extentions.db.init_app(app)
csrf = CSRFProtect(app)



with app.app_context():
    extentions.db.create_all()



if __name__ == "__main__":
    app.run(debug= True)