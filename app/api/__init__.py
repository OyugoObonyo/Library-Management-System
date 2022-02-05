from flask import Blueprint

bp = Blueprint('api', __name__)

from app.api.v1.routes.books import *
from app.api.v1.routes.users import *
