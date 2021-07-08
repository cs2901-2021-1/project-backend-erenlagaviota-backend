from flask.blueprints import Blueprint
from .blueprints.numericalProjection import numericalProjection

api = Blueprint('api',__name__)

api.register_blueprint(numericalProjection,url_prefix='/numerical')


    # @app.route('/hello')
    # def test():
    #     test_core = Core()
    #     return str(int(xd.getProjection('AM0001')))  # type: ignore
