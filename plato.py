import os
from .src.user.infrastructure.user_providers import UserProviders
from .src import user
from .src.shared.plato_command_bus import PlatoCommandBus
from .src.user.application.command.create_user_command import CreateUserCommand
from .src.user.application.command.create_user_handler import CreateUserCommandHandler
from .src.user.infrastructure.controller.user_controller import userFlaskBlueprint
from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

load_dotenv()
userProvider = UserProviders()
userProvider.wire(packages=[user])

PlatoCommandBus.subscribe(CreateUserCommand, CreateUserCommandHandler())

app = Flask(__name__)
app.register_blueprint(userFlaskBlueprint)

app.config["JWT_SECRET_KEY"] = os.environ["JWT_SECRET_KEY"]
JWTManager(app)

SWAGGER_URL = ''
API_URL = '/static/swagger.yaml'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Plato API"
    }
)

app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
