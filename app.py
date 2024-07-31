from flask import Flask
from flask_wtf.csrf import CSRFProtect
from blueprints.general import app as general
from blueprints.admin import app as admin
from blueprints.user import app as user
import config
import extentions
from models.user import User

app = Flask(__name__)
app.register_blueprint(general)
app.register_blueprint(admin)
app.register_blueprint(user)


app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
app.config["SECRET_KEY"] = config.SECRET_KEY
extentions.db.init_app(app)
csrf = CSRFProtect(app)



with app.app_context():
    extentions.db.create_all()



if __name__ == "__main__":
    app.run(debug= True)