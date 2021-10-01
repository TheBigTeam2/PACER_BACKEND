from dao.AvaliacaoDao import AvaliacaoDao
from flask import Blueprint, request, jsonify, make_response
from services.AvaliacaoService import AvaliacaoService

avaliacao_service = AvaliacaoService()
avaliacao_dao = AvaliacaoDao()
avaliacao = Blueprint("avaliacao",__name__)


@avaliacao.get('/avaliacao')
def get_avaliacao():

    if request.args['avaliador']:
        id_avaliador = request.args['avaliador']
        return jsonify(avaliacao_dao.get_all_avaliacoes_by_avaliador(id_avaliador))

@avaliacao.post('/avaliacao')
def post_avaliacao():

    avaliacoes = request.get_json()

    try:

        avaliacao_service.create_avaliacoes(avaliacoes)
        response =  make_response(jsonify({"status":"Created avaliacoes"}),201)
        return response

    except Exception as error:
        raise error
    

