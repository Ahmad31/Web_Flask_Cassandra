
import uuid
import os
from flask_login import LoginManager
from flask import Flask
from cassandra.cluster import Cluster
from flask_cqlalchemy import CQLAlchemy

app = Flask(__name__)
app.config['CASSANDRA_HOSTS'] = ['172.17.0.2','172.17.0.3','172.17.0.4']
app.config['CASSANDRA_KEYSPACE'] = "project"
CQLENG_ALLOW_SCHEMA_MANAGEMENT = 'CQLENG_ALLOW_SCHEMA_MANAGEMENT'
app.config['SECRET_KEY'] = "random string"
db = CQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


from app import views, models
