import json
from flask.blueprints import Blueprint
from flask.wrappers import Response
from flask import jsonify
from ...data.collector.collector import Collector
from ...security.security import auth_required

getCursos = Blueprint('getCursos', __name__)


@getCursos.route('/valid', methods=['GET'])
@auth_required
def getValidCursos():
    collector = Collector()
    cursosJSON = collector.getCursos()
    if cursosJSON is not None:
        return jsonify(json.loads(cursosJSON))
