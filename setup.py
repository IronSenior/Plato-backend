from distutils.core import setup

setup(
  name='plato',
  packages=['plato'],
  version='0.1',
  license='GPL-3',
  description='Plato API',
  author='Pepe Márquez Doblas',
  author_email='pepemarquezof@gmail.com',
  url='https://github.com/IronSenior/Plato-backend',
  entry_points={
      "console_scripts": [
          "plato = plato.main:main"
      ]
  },
  install_requires=[
    "eventsourcing==9.0.1",
    "passlib==1.7.4",
    "dependency-injector==4.31.2",
    "event-bus==1.0.2",
    "flask-swagger-ui==3.36.0",
    "python-dotenv==0.17.0",
    "Flask==2.0.1",
    "Flask-Cors==3.0.10",
    "tweepy==3.10.0",
    "Flask-JWT-Extended==4.2.3",
    "pymongo==3.12.0",
    "SQLAlchemy==1.4.25",
    "plato-cqrs",
    "flask-crontab==0.1.2",
    "waitress==2.0.0",
    "Faker==9.2.0",
  ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
    'Programming Language :: Python :: 3.9'
  ],
)
