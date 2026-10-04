"""Routes for Reports and Queries (C226C / F-013 and F-014)
Consulta de Órgãos com Relatório (C226C - F-013)
Consulta de Justificativas (C250C - F-014)
Operações: CON (consulta leitura-apenas)
Funcionalidade: Listagem + Pedido de relatório (fila de impressão)
Auditoria: Consulta registrada
"""
from flask import Blueprint, render_template, request, jsonify
from app.models.bairro import BAIRRO
from app.models.unidade import UNIDADE_ORCAMENTARIA
from app.models.grupo import GRUPO
from app.models.fonte import FONTE_RECURSOS
from app.models.auditoria import AUDITORIA
from app.models.historico import HISTORICO_PERIODO_ORGAO
from app.config import Config

bp = Blueprint('consulta', __name__, url_prefix='/consulta')

@bp.route('/', methods=['GET'])
def index():
    """Página principal de consultas"""
    return render_template('consulta/index.html')

@bp.route('/auditoria', methods=['GET'])
def auditoria():
    """Consulta de Auditoria - leitura apenas"""
    page = request.args.get('page', 1, type=int)
    pagination = AUDITORIA.query.order_by(AUDITORIA.data_operacao.desc()).paginate(page=page, per_page=Config.ITEMS_PER_PAGE)
    
    # Auditoria: Registrar consultoria
    try:
        from app import db
        audit_rec = AUDITORIA.registrar(
            tabela='auditoria',
            operacao='CONSULTA',
            chave_primaria='*',
            usuario=request.remote_addr
        )
        db.session.add(audit_rec)
        db.session.commit()
    except:
        pass
    
    return render_template('consulta/auditoria.html', 
                         auditorias=pagination.items, 
                         pagination=pagination,
                         page=page)

@bp.route('/historico', methods=['GET'])
def historico():
    """Consulta de Histórico de Períodos e Órgãos - leitura apenas"""
    page = request.args.get('page', 1, type=int)
    pagination = HISTORICO_PERIODO_ORGAO.query.order_by(
        HISTORICO_PERIODO_ORGAO.data_mudanca.desc()
    ).paginate(page=page, per_page=Config.ITEMS_PER_PAGE)
    
    return render_template('consulta/historico.html', 
                         historicos=pagination.items, 
                         pagination=pagination,
                         page=page)

@bp.route('/unidades', methods=['GET'])
def unidades():
    """Consulta de Unidades Orçamentárias - leitura apenas"""
    page = request.args.get('page', 1, type=int)
    pagination = UNIDADE_ORCAMENTARIA.query.order_by(UNIDADE_ORCAMENTARIA.codigo_unidade).paginate(page=page, per_page=Config.ITEMS_PER_PAGE)
    return render_template('consulta/unidades.html', 
                         unidades=pagination.items, 
                         pagination=pagination,
                         page=page)

@bp.route('/bairros', methods=['GET'])
def bairros():
    """Consulta de Bairros - leitura apenas"""
    page = request.args.get('page', 1, type=int)
    pagination = BAIRRO.query.order_by(BAIRRO.codigo_bairro).paginate(page=page, per_page=Config.ITEMS_PER_PAGE)
    return render_template('consulta/bairros.html', 
                         bairros=pagination.items, 
                         pagination=pagination,
                         page=page)

@bp.route('/grupos', methods=['GET'])
def grupos():
    """Consulta de Grupos - leitura apenas"""
    page = request.args.get('page', 1, type=int)
    pagination = GRUPO.query.order_by(GRUPO.codigo_grupo, GRUPO.tipo_orgao).paginate(page=page, per_page=Config.ITEMS_PER_PAGE)
    return render_template('consulta/grupos.html', 
                         grupos=pagination.items, 
                         pagination=pagination,
                         page=page)

@bp.route('/fontes', methods=['GET'])
def fontes():
    """F-004: Consulta de Fontes de Recursos - leitura apenas"""
    page = request.args.get('page', 1, type=int)
    pagination = FONTE_RECURSOS.query.order_by(FONTE_RECURSOS.codigo_fonte).paginate(page=page, per_page=Config.ITEMS_PER_PAGE)
    return render_template('consulta/fontes.html', 
                         fontes=pagination.items, 
                         pagination=pagination,
                         page=page)

@bp.route('/contas', methods=['GET'])
def contas():
    """Consulta de Contas Classificadas - leitura apenas"""
    from app.models.conta import CONTA_CLASSIFICADA
    page = request.args.get('page', 1, type=int)
    pagination = CONTA_CLASSIFICADA.query.order_by(CONTA_CLASSIFICADA.conta).paginate(page=page, per_page=Config.ITEMS_PER_PAGE)
    return render_template('consulta/contas.html', 
                         contas=pagination.items, 
                         pagination=pagination,
                         page=page)

@bp.route('/orgaos', methods=['GET'])
def orgaos():
    """F-013: Consulta de Órgãos com Relatório (C226C) - leitura apenas"""
    page = request.args.get('page', 1, type=int)
    # TODO: Filtrar por coordenação regional em sessão quando implementada
    # Consulta básica de órgãos (modelo não disponível ainda)
    return render_template('consulta/orgaos.html', 
                         page=page,
                         mensagem='Esta é uma consulta de apenas leitura. Use o botão "Pedir Relatório" para solicitar impressão.')

@bp.route('/justificativas', methods=['GET'])
def justificativas():
    """F-014: Consulta de Justificativas (C250C) - leitura apenas"""
    page = request.args.get('page', 1, type=int)
    # TODO: Filtrar por tipo_orgao em sessão quando implementada
    # Consulta básica de justificativas (modelo não disponível ainda)
    return render_template('consulta/justificativas.html',
                         page=page,
                         mensagem='Esta é uma consulta de apenas leitura. Use o botão "Pedir Relatório" para solicitar impressão.')

@bp.route('/api/auditoria', methods=['GET'])
def api_auditoria():
    """API: Retornar últimas auditarias em JSON"""
    limit = request.args.get('limit', 100, type=int)
    auditorias = AUDITORIA.query.order_by(AUDITORIA.data_operacao.desc()).limit(limit).all()
    return jsonify([a.to_dict() for a in auditorias])

@bp.route('/api/resumo', methods=['GET'])
def api_resumo():
    """API: Retornar resumo de todos os cadastros"""
    return jsonify({
        'unidades': UNIDADE_ORCAMENTARIA.query.count(),
        'bairros': BAIRRO.query.count(),
        'grupos': GRUPO.query.count(),
        'fontes': FONTE_RECURSOS.query.count(),
        'auditoria': AUDITORIA.query.count(),
        'historico': HISTORICO_PERIODO_ORGAO.query.count(),
    })

@bp.route('/api/pedir-relatorio', methods=['POST'])
def pedir_relatorio():
    """API: Adicionar pedido de relatório à fila de impressão"""
    # TODO: Implementar fila de impressão
    return jsonify({'status': 'Pedido recebido', 'mensagem': 'Seu relatório foi adicionado à fila de impressão'})
