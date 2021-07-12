from flask.blueprints import Blueprint
from .blueprints.numericalProjection import numericalProjection

api = Blueprint('api',__name__)

api.register_blueprint(numericalProjection,url_prefix='/numerical')
