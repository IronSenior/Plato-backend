import datetime
import os
from waitress import serve

# * Dependency injection wiring
from .src import user, brand, twitter
from .src.user.infrastructure.user_providers import UserProviders
from .src.brand.infrastructure.brand_providers import BrandProviders
from .src.twitter.infrastructure.twitter_providers import TwitterProviders

# * Command Bus Configuration
from .src.shared.infrastructure.plato_command_bus import PlatoCommandBus
from .src.user.application.command.create_user_command import CreateUserCommand
from .src.user.application.command.create_user_handler import CreateUserCommandHandler
from .src.brand.application.command.create_brand_command import CreateBrandCommand
from .src.brand.application.command.create_brand_handler import CreateBrandHandler
from .src.twitter.application.command.schedule_tweet_command import ScheduleTweetCommand
from .src.twitter.application.command.schedule_tweet_handler import ScheduleTweetHandler
from .src.twitter.application.command.add_account_command import AddAccountCommand
from .src.twitter.application.command.add_account_handler import AddAccountHandler
from .src.twitter.application.command.publish_tweet_command import PublishTweetCommand
from .src.twitter.application.command.publish_tweet_handler import PublishTweetHandler
from .src.twitter.application.command.create_tweet_report_command import CreateTweetReportCommand
from .src.twitter.application.command.create_tweet_report_handler import CreateTweetReportHandler
from .src.twitter.application.command.create_account_report_command import CreateAccountReportCommand
from .src.twitter.application.command.create_account_report_handler import CreateAccountReportHandler
from .src.twitter.application.command.add_tweet_media_command import AddTweetMediaCommand
from .src.twitter.application.command.add_tweet_media_handler import AddTweetMediaHandler

# * Query Bus Configuration
from .src.shared.infrastructure.plato_query_bus import PlatoQueryBus
from .src.user.application.query.get_user_by_email_query import GetUserByEmailQuery
from .src.user.application.query.get_user_by_email_handler import GetUserByEmailHandler
from .src.twitter.application.query.get_account_query import GetAccountQuery
from .src.twitter.application.query.get_account_handler import GetAccountHandler
from .src.twitter.application.query.get_account_by_brand_query import GetAccountByBrandQuery
from .src.twitter.application.query.get_account_by_brand_handler import GetAccountByBrandHandler
from .src.user.application.query.get_user_query import GetUserQuery
from .src.user.application.query.get_user_handler import GetUserHandler
from .src.brand.application.query.get_brand_by_user_id_query import GetBrandByUserIdQuery
from .src.brand.application.query.get_brand_by_user_id_handler import GetBrandByUserIdHandler
from .src.twitter.application.query.get_pending_tweets_query import GetPendingTweetsQuery
from .src.twitter.application.query.get_pending_tweets_handler import GetPendingTweetsHandler
from .src.twitter.application.query.get_tweets_by_account_query import GetTweetsByAccountQuery
from .src.twitter.application.query.get_tweets_by_account_handler import GetTweetsByAccountHandler
from .src.twitter.application.query.get_published_tweets_handler import GetPublishedTweetsHandler
from .src.twitter.application.query.get_published_tweets_query import GetPublishedTweetsQuery
from .src.twitter.application.query.get_tweet_report_by_tweet_query import GetTweetReportsByTweetQuery
from .src.twitter.application.query.get_tweet_report_by_tweet_handler import GetTweetReportsByTweetHandler
from .src.twitter.application.query.get_tweet_query import GetTweetQuery
from .src.twitter.application.query.get_tweet_handler import GetTweetHandler
from .src.twitter.application.query.get_all_accounts_query import GetAllAccountsQuery
from .src.twitter.application.query.get_all_accounts_handler import GetAllAccountsHandler
from .src.twitter.application.query.get_account_reports_by_account_handler import GetAccountReportsByAccountHandler
from .src.twitter.application.query.get_account_reports_by_account_query import GetAccountReportsByAccountQuery

# * Event Bus configuration
from .src.brand.infrastructure.read_model.on_brand_was_created import onBrandWasCreated
from .src.twitter.infrastructure.read_model.on_account_was_added import onTwitterAccountWasCreated
from .src.twitter.infrastructure.read_model.on_tweet_was_scheduled import onTweetWasScheduled
from .src.twitter.infrastructure.read_model.on_tweet_was_published import onTweetWasPublished

# * Flask Configuration
from flask import Flask
from flask_cors import CORS
from .src.user.infrastructure.controller.user_controller import userFlaskBlueprint
from .src.brand.infrastructure.controller.brand_controller import brandFlaskBlueprint
from .src.twitter.infrastructure.controller.twitter_controller import twitterFlaskBlueprint
from .src.twitter.infrastructure.controller.twitter_controller import publish_scheduled_tweets
from .src.twitter.infrastructure.controller.twitter_controller import generate_tweets_reports
from .src.twitter.infrastructure.controller.twitter_controller import generate_account_reports
from .src.shared.infrastructure.json_web_token_conf import jwtManager
from flask_crontab import Crontab
from flask_swagger_ui import get_swaggerui_blueprint
from .DB.regenerate_mongo_db import main as regenerateDB

userProvider = UserProviders()
userProvider.wire(packages=[user])
brandProvider = BrandProviders()
brandProvider.wire(packages=[brand])
twitterProvider = TwitterProviders()
twitterProvider.wire(packages=[twitter])

crontab = Crontab()


def create_app(test_env=False):
    if test_env or os.environ["ENV_MODE"] == "Test":
        regenerateDB()
    
    PlatoQueryBus.clean()
    PlatoCommandBus.clean()

    PlatoQueryBus.subscribe(GetUserByEmailQuery, GetUserByEmailHandler())
    PlatoQueryBus.subscribe(GetUserQuery, GetUserHandler())
    PlatoQueryBus.subscribe(GetBrandByUserIdQuery, GetBrandByUserIdHandler())
    PlatoQueryBus.subscribe(GetAccountQuery, GetAccountHandler())
    PlatoQueryBus.subscribe(GetAccountByBrandQuery, GetAccountByBrandHandler())
    PlatoQueryBus.subscribe(GetPendingTweetsQuery, GetPendingTweetsHandler())
    PlatoQueryBus.subscribe(GetTweetsByAccountQuery, GetTweetsByAccountHandler())
    PlatoQueryBus.subscribe(GetPublishedTweetsQuery, GetPublishedTweetsHandler())
    PlatoQueryBus.subscribe(GetTweetReportsByTweetQuery, GetTweetReportsByTweetHandler())
    PlatoQueryBus.subscribe(GetTweetQuery, GetTweetHandler())
    PlatoQueryBus.subscribe(GetAllAccountsQuery, GetAllAccountsHandler())
    PlatoQueryBus.subscribe(GetAccountReportsByAccountQuery, GetAccountReportsByAccountHandler())

    PlatoCommandBus.subscribe(CreateUserCommand, CreateUserCommandHandler())
    PlatoCommandBus.subscribe(CreateBrandCommand, CreateBrandHandler())
    PlatoCommandBus.subscribe(AddAccountCommand, AddAccountHandler())
    PlatoCommandBus.subscribe(ScheduleTweetCommand, ScheduleTweetHandler())
    PlatoCommandBus.subscribe(PublishTweetCommand, PublishTweetHandler())
    PlatoCommandBus.subscribe(CreateTweetReportCommand, CreateTweetReportHandler())
    PlatoCommandBus.subscribe(CreateAccountReportCommand, CreateAccountReportHandler())
    PlatoCommandBus.subscribe(AddTweetMediaCommand, AddTweetMediaHandler())

    app = Flask(__name__)
    app.register_blueprint(userFlaskBlueprint)
    app.register_blueprint(brandFlaskBlueprint)
    app.register_blueprint(twitterFlaskBlueprint)
    crontab.init_app(app)
    
    CORS(app)

    app.config["JWT_SECRET_KEY"] = os.environ["JWT_SECRET_KEY"]
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(days=14)
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
    return app

@crontab.job(minute="*")
def pusblish_tweet_cron():
    publish_scheduled_tweets()
    
@crontab.job(minute="*/5")
def generate_tweet_reports_cron():
    generate_tweets_reports()
    
@crontab.job(minute="0")
def generate_account_reports_cron():
    generate_account_reports()
    
def main():
    app = create_app()
    if os.environ["FLASK_ENV"] == "development":
        app.run(host="localhost", port="8080")
    else:
        serve(app, port="8080")

if __name__ == '__main__':
    main()
