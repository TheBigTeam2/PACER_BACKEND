from flask.blueprints import Blueprint
from dao.CriterioDao import CriterioDao
from flask import request, jsonify, make_response

criterio_dao = CriterioDao()
criterio = Blueprint("criterio",__name__)

@criterio.get('/criterios')
def get_alunos():

    return jsonify(criterio_dao.get_all_criterios())

@criterio.post('/criterios')
def insert():

    criterio = request.get_json()

    try:
        insertion_result = criterio_dao.save_criterio(criterio)

        if insertion_result:

            response =  make_response(jsonify({"inserted_content":criterio}),201)
            return response

    except Exception as error:
        raise error
    
@criterio.put('/criterios')
def update():

    criterio = request.get_json()

    if request.args['id']:
        criterio_id = request.args['id']
        try:
            update_result = criterio_dao.update_criterio(criterio_id)

            if update_result:

                response =  make_response(jsonify({"inserted_content":criterio}),201)
                return response

        except Exception as error:
            raise error

@criterio.delete('/criterios')
def delete():

    criterio = request.get_json()

    if request.args['id']:
        criterio_id = request.args['id']
        try:
            delete_result = criterio_dao.delete_criterio(criterio_id)

            if delete_result:

                response =  make_response(jsonify({"inserted_content":criterio}),201)
                return response

        except Exception as error:
            raise error