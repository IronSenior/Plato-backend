import os
from .src.user.infrastructure.user_providers import UserProviders
from .src.socialNetworkGroup.infrastructure.sn_group_providers import SNGroupProviders
from .src import user, socialNetworkGroup
from .src.shared.plato_command_bus import PlatoCommandBus
from .src.user.application.command.create_user_command import CreateUserCommand
from .src.user.application.command.create_user_handler import CreateUserCommandHandler
from .src.socialNetworkGroup.application.command.create_social_network_group_command import CreateSocialNetworkGroupCommand
from .src.socialNetworkGroup.application.command.create_social_network_group_handler import CreateSocialNetworkGroupHandler
from .src.user.infrastructure.controller.user_controller import userFlaskBlueprint
from .src.socialNetworkGroup.infrastructure.controller.sn_group_controller import snGroupFlaskBlueprint
from flask import Flask
from .src.shared.json_web_token_conf import jwtManager
from flask_swagger_ui import get_swaggerui_blueprint
from dotenv import load_dotenv

load_dotenv()
userProvider = UserProviders()
userProvider.wire(packages=[user])

snGroupProvider = SNGroupProviders()
snGroupProvider.wire(packages=[socialNetworkGroup])

PlatoCommandBus.subscribe(CreateUserCommand, CreateUserCommandHandler())
PlatoCommandBus.subscribe(CreateSocialNetworkGroupCommand, CreateSocialNetworkGroupHandler())

app = Flask(__name__)
app.register_blueprint(userFlaskBlueprint)
app.register_blueprint(snGroupFlaskBlueprint)

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
