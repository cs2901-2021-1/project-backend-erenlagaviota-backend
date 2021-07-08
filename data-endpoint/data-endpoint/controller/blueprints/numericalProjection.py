from flask.blueprints import Blueprint
from flask import request
from ...data.core.core import Core
from ...security.security import auth_required

numericalProjection = Blueprint('numericalProjection',__name__)

@numericalProjection.route('/data')
@auth_required
def getNumericalProjection():
    body = request.json
    course = body['course']  # type: ignore
    core = Core()
    projection = core.getProjection(course)
    return str(int(projection))  # type: ignore
