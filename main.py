import os
from .src.user.infrastructure.user_providers import UserProviders
from .src.brand.infrastructure.brand_providers import BrandProviders
from .src import user, brand, twitter
from .src.shared.infrastructure.plato_command_bus import PlatoCommandBus
from .src.user.application.command.create_user_command import CreateUserCommand
from .src.user.application.command.create_user_handler import CreateUserCommandHandler
from .src.brand.application.command.create_brand_command import CreateBrandCommand
from .src.brand.application.command.create_brand_handler import CreateBrandHandler
from .src.user.infrastructure.controller.user_controller import userFlaskBlueprint
from .src.brand.infrastructure.controller.brand_controller import brandFlaskBlueprint
from .src.twitter.infrastructure.controller.twitter_controller import twitterFlaskBlueprint
from .src.twitter.infrastructure.twitter_providers import TwitterProviders
from .src.twitter.application.command.shedule_tweet_command import ScheduleTweetCommand
from .src.twitter.application.command.shedule_tweet_handler import ScheduleTweetHandler
from .src.twitter.application.command.add_account_command import AddAccountCommand
from .src.twitter.application.command.add_account_handler import AddAccountHandler
from flask import Flask
from .src.shared.infrastructure.json_web_token_conf import jwtManager
from flask_swagger_ui import get_swaggerui_blueprint
from dotenv import load_dotenv
from flask_crontab import Crontab

load_dotenv()
userProvider = UserProviders()
userProvider.wire(packages=[user])

brandProvider = BrandProviders()
brandProvider.wire(packages=[brand])

twitterProvider = TwitterProviders()
twitterProvider.wire(packages=[twitter])

PlatoCommandBus.subscribe(CreateUserCommand, CreateUserCommandHandler())
PlatoCommandBus.subscribe(CreateBrandCommand, CreateBrandHandler())
PlatoCommandBus.subscribe(AddAccountCommand, AddAccountHandler())
PlatoCommandBus.subscribe(ScheduleTweetCommand, ScheduleTweetHandler())

app = Flask(__name__)
app.register_blueprint(userFlaskBlueprint)
app.register_blueprint(brandFlaskBlueprint)
app.register_blueprint(twitterFlaskBlueprint)

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
