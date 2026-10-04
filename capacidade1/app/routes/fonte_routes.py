"""Routes for Sources (C144T) - F-004
Manter Fontes de Recursos
Operações: CON APENAS (READ-ONLY)
NÃO implementar: criar(), editar(), deletar()
Validações: RN-01 (7d código), RN-02 (desc 30c), RN-03 (código órgão parte da chave),
            RN-04 (ind_FNDE opcional S/N)
"""
from flask import Blueprint, render_template, request, jsonify
from app.models.fonte import FONTE_RECURSOS
from app.models.auditoria import AUDITORIA
from app.config import Config

bp = Blueprint('fonte', __name__, url_prefix='/fonte')

@bp.route('/', methods=['GET'])
def listar():
    """F-004: Consultar fontes de recursos do órgão (filtrado por sessão)"""
    page = request.args.get('page', 1, type=int)
    # TODO: Filtrar por código_orgao da sessão quando sessão implementada
    pagination = FONTE_RECURSOS.query.order_by(FONTE_RECURSOS.codigo_fonte).paginate(page=page, per_page=Config.ITEMS_PER_PAGE)
    
    # Auditoria: Registrar consultoria
    if pagination.items:
        auditoria = AUDITORIA.registrar(
            tabela='fonte_recursos',
            operacao='CONSULTA',
            chave_primaria='*',
            usuario=request.remote_addr
        )
        try:
            from app import db
            db.session.add(auditoria)
            db.session.commit()
        except:
            pass  # Consultoria não grava por design se erro
    
    return render_template('fonte/lista.html', 
                         fontes=pagination.items, 
                         pagination=pagination, 
                         page=page,
                         mensagem_readonly='Esta é uma consulta de apenas leitura. Criar/editar/deletar fontes não é permitido.')

@bp.route('/detalhes/<codigo_fonte>/<codigo_orgao>', methods=['GET'])
def detalhes(codigo_fonte, codigo_orgao):
    """F-004: Ver detalhes de uma fonte (READ-ONLY)"""
    fonte = FONTE_RECURSOS.query.filter_by(codigo_fonte=codigo_fonte, codigo_orgao=codigo_orgao).first()
    if not fonte:
        return jsonify({'error': 'Fonte não encontrada'}), 404
    
    # Auditoria: Registrar consultoria
    auditoria = AUDITORIA.registrar(
        tabela='fonte_recursos',
        operacao='CONSULTA',
        chave_primaria=f"{codigo_fonte}-{codigo_orgao}",
        usuario=request.remote_addr
    )
    try:
        from app import db
        db.session.add(auditoria)
        db.session.commit()
    except:
        pass
    
    return render_template('fonte/detalhes.html', 
                         fonte=fonte,
                         mensagem_readonly='Esta é uma consulta de apenas leitura.')

@bp.route('/api/<codigo_fonte>/<codigo_orgao>', methods=['GET'])
def get_json(codigo_fonte, codigo_orgao):
    """F-004: API - Retornar fonte em JSON (READ-ONLY)"""
    fonte = FONTE_RECURSOS.query.filter_by(codigo_fonte=codigo_fonte, codigo_orgao=codigo_orgao).first()
    if not fonte:
        return jsonify({'error': 'Fonte não encontrada'}), 404
    return jsonify(fonte.to_dict())
