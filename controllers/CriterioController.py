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

    if request.args['id']:
        id_criterio = request.args['id']
        criterio_json = request.get_json()
        criterio = criterio_dao.get_criterio_by_id(id_criterio)

        if criterio:
            criterio_dao.update_criterio(id_criterio,criterio_json)
            response = make_response(jsonify({"updated_register":id_criterio}),200)

        else:
            response = make_response(jsonify({"error":"register not found"}),500)
   
    else:
        response = make_response(jsonify({"error":"id argument empty"}),500)

    return response

@criterio.delete('/criterios')
def delete():

    if request.args['id']:
        id_criterio = request.args['id']
        criterio_json = request.get_json()
        criterio = criterio_dao.get_criterio_by_id(id_criterio)

        if criterio:
            resp = criterio_dao.delete_criterio(id_criterio)
            if (resp):
                response = make_response(jsonify({"deleted_register":id_criterio}),200)

            else:
                response = make_response(jsonify({"error":resp}),500)
   
        else:
            response = make_response(jsonify({"error":"id argument empty"}),500)

    return response