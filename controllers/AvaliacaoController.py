from flask import Blueprint, request, jsonify
from dao.AvaliacaoDao import AvaliacaoDao

avaliacao_dao = AvaliacaoDao()
avaliacao = Blueprint("avaliacao",__name__)


@avaliacao.get('/avaliacao')
def get_avaliacao():

    if request.args['avaliador']:
        id_avaliador = request.args['avaliador']
        return jsonify(avaliacao_dao.get_all_avaliacoes_by_avaliador(id_avaliador))



