import json
from flask.blueprints import Blueprint
from flask import request
from flask.wrappers import Response
from ...data.core.core import Core
from ...security.security import auth_required

numericalProjection = Blueprint('numericalProjection', __name__)


@numericalProjection.route('/data', methods=['POST'])
@auth_required
def getNumericalProjection():
    body = request.json
    course = body['course']  # type: ignore
    onDemand = body['onDemand']  # type: ignore
    shouldUpdate = False
    if onDemand == "true":
        shouldUpdate = True
    elif onDemand == "false":
        shouldUpdate = False
    core = Core(course=course, shouldOnDemand=shouldUpdate)
    projection = core.getProjection(course)
    # type: ignore
    return Response(json.dumps({'numericalProjection': projection}), mimetype='application/json', status=200)
