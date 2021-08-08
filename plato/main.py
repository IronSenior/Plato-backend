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
from .src.twitter.application.command.publish_tweet_command import PublishTweetCommand
from .src.twitter.application.command.publish_tweet_handler import PublishTweetHandler
from .src.shared.infrastructure.plato_query_bus import PlatoQueryBus
from .src.user.application.query.get_user_by_email_query import GetUserByEmailQuery
from .src.user.application.query.get_user_by_email_handler import GetUserByEmailHandler
from .src.twitter.application.query.get_account_query import GetAccountQuery
from .src.twitter.application.query.get_account_handler import GetAccountHandler
from .src.user.application.query.get_user_query import GetUserQuery
from .src.user.application.query.get_user_handler import GetUserHandler
from .src.brand.application.query.get_brand_by_user_id_query import GetBrandByUserIdQuery
from .src.brand.application.query.get_brand_by_user_id_handler import GetBrandByUserIdHandler
from flask import Flask
from .src.shared.infrastructure.json_web_token_conf import jwtManager
from flask_swagger_ui import get_swaggerui_blueprint
from dotenv import load_dotenv

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
PlatoCommandBus.subscribe(PublishTweetCommand, PublishTweetHandler())

PlatoQueryBus.subscribe(GetUserByEmailQuery, GetUserByEmailHandler())
PlatoQueryBus.subscribe(GetUserQuery, GetUserHandler())
PlatoQueryBus.subscribe(GetBrandByUserIdQuery, GetBrandByUserIdHandler())
PlatoQueryBus.subscribe(GetAccountQuery, GetAccountHandler())

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
