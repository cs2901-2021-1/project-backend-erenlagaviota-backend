from flask.blueprints import Blueprint
from .blueprints.numericalProjection import numericalProjection
from .blueprints.getCursos import getCursos

api = Blueprint('api',__name__)

api.register_blueprint(numericalProjection,url_prefix='/numerical')
api.register_blueprint(getCursos,url_prefix='/cursos')
