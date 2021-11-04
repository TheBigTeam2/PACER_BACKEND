from flask import Blueprint, request, jsonify, make_response
from dao.AvaliacaoDao import AvaliacaoDao

avaliacao = Blueprint("avaliacao",__name__)


@avaliacao.get('/avaliacao')
def get_avaliacao():
    avaliacao_dao = AvaliacaoDao()
    if request.args['avaliador']:
        id_avaliador = request.args['avaliador']
        return jsonify(avaliacao_dao.get_all_avaliacoes_by_avaliador(id_avaliador))

@avaliacao.post('/avaliacao')
def post_avaliacao():
    avaliacao_dao = AvaliacaoDao()
    avaliacao = request.get_json()

    try:
        insertion_result = avaliacao_dao.save_avaliacao_in_mass(avaliacao)

        if insertion_result:

            response =  make_response(jsonify({"inserted_content":avaliacao}),201)
            return response

    except Exception as error:
        raise error
    

