import os
from .src.user.infrastructure.user_providers import UserProviders
from .src.brand.infrastructure.brand_providers import BrandProviders
from .src import user, brand
from .src.shared.infrastructure.plato_command_bus import PlatoCommandBus
from .src.user.application.command.create_user_command import CreateUserCommand
from .src.user.application.command.create_user_handler import CreateUserCommandHandler
from .src.brand.application.command.create_brand_command import CreateBrandCommand
from .src.brand.application.command.create_brand_handler import CreateBrandHandler
from .src.user.infrastructure.controller.user_controller import userFlaskBlueprint
from .src.brand.infrastructure.controller.brand_controller import brandFlaskBlueprint
from flask import Flask
from .src.shared.infrastructure.json_web_token_conf import jwtManager
from flask_swagger_ui import get_swaggerui_blueprint
from dotenv import load_dotenv

load_dotenv()
userProvider = UserProviders()
userProvider.wire(packages=[user])

brandProvider = BrandProviders()
brandProvider.wire(packages=[brand])

PlatoCommandBus.subscribe(CreateUserCommand, CreateUserCommandHandler())
PlatoCommandBus.subscribe(CreateBrandCommand, CreateBrandHandler())

app = Flask(__name__)
app.register_blueprint(userFlaskBlueprint)
app.register_blueprint(brandFlaskBlueprint)

app.config["JWT_SECRET_KEY"] = os.environ["JWT_SECRET_KEY"]
jwtManager.init_app(app)

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
