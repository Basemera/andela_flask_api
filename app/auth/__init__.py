from app.app import app
from app.auth.views import auth_blueprint
app.register_blueprint(auth_blueprint)