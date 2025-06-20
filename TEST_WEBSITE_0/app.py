from flask import Flask
from flask_login import LoginManager
from auth.models import User
from auth.views import auth_bp
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key'

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

# Register Blueprint
app.register_blueprint(auth_bp)

if __name__ == '__main__':
    if not os.path.exists('database.db'):
        from auth.db import init_db
        init_db()
    app.run(debug=True)
