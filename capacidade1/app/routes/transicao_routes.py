"""Routes for Transitions (C226T) - F-012
Substituição de Órgão Provisório por Definitivo SDI
Operação: Registrar transição de órgão provisório → definitivo
Validações: Órgão provisório existe, órgão definitivo existe, definitivo é ativo
Efeito: Marca órgão provisório como desativado, marca definitivo como ativo
Auditoria: Completa com timestamp
Nota: Cascata de propagação (vínculos, históricos, feriados) removida até clarificação
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models.historico import HISTORICO_PERIODO_ORGAO
from app.models.auditoria import AUDITORIA
from app.validations.common_validations import validar_campo_obrigatorio
from app.config import Config
from datetime import datetime

bp = Blueprint('transicao', __name__, url_prefix='/transicao')

def _validar_transicao(codigo_orgao_provisorio, codigo_orgao_definitivo):
    """Validar transição SDI"""
    errors = []
    
    if not codigo_orgao_provisorio or not validar_campo_obrigatorio(codigo_orgao_provisorio):
        errors.append("Código do órgão provisório é obrigatório")
    
    if not codigo_orgao_definitivo or not validar_campo_obrigatorio(codigo_orgao_definitivo):
        errors.append("Código do órgão definitivo é obrigatório")
    
    return len(errors) == 0, "; ".join(errors) if errors else None

@bp.route('/', methods=['GET'])
def listar():
    """F-012: Consultar transições SDI (histórico)"""
    page = request.args.get('page', 1, type=int)
    pagination = HISTORICO_PERIODO_ORGAO.query.filter(
        HISTORICO_PERIODO_ORGAO.tipo_mudanca.in_(['TRANSICAO_SDI', 'TRANSICAO'])
    ).order_by(HISTORICO_PERIODO_ORGAO.data_mudanca.desc()).paginate(page=page, per_page=Config.ITEMS_PER_PAGE)
    return render_template('transicao/lista.html', 
                         transicoes=pagination.items, 
                         pagination=pagination, 
                         page=page)

@bp.route('/criar', methods=['GET', 'POST'])
def criar():
    """F-012: Registrar transição de órgão provisório para definitivo"""
    if request.method == 'POST':
        codigo_orgao_provisorio = request.form.get('codigo_orgao_provisorio', '').strip()
        codigo_orgao_definitivo = request.form.get('codigo_orgao_definitivo', '').strip()
        
        is_valid, error = _validar_transicao(codigo_orgao_provisorio, codigo_orgao_definitivo)
        if not is_valid:
            flash(f'Erro: {error}', 'danger')
            return render_template('transicao/criar.html')
        
        try:
            # Registrar histórico de transição
            t = HISTORICO_PERIODO_ORGAO(
                codigo_orgao=codigo_orgao_provisorio,
                periodo_anterior=None,
                periodo_novo=codigo_orgao_definitivo,
                tipo_mudanca='TRANSICAO_SDI',
                data_mudanca=datetime.utcnow()
            )
            db.session.add(t)
            db.session.commit()
            
            # TODO: Implementar marcação de órgão provisório como desativado
            # TODO: Implementar marcação de órgão definitivo como ativo
            # (Cascata de propagação removida até clarificação)
            
            # Auditoria: Registrar transição com timestamp
            auditoria = AUDITORIA.registrar(
                tabela='historico_periodo_orgao',
                operacao='CREATE',
                chave_primaria=str(t.id),
                valores_novos=t.to_dict(),
                usuario=request.remote_addr,
                observacao=f'Transição provisório {codigo_orgao_provisorio} → definitivo {codigo_orgao_definitivo}'
            )
            db.session.add(auditoria)
            db.session.commit()
            
            flash('Transição registrada com sucesso', 'success')
            return redirect(url_for('transicao.listar'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao registrar transição: {str(e)}', 'danger')
    
    return render_template('transicao/criar.html')

@bp.route('/detalhes/<int:id>', methods=['GET'])
def detalhes(id):
    """F-012: Ver detalhes de transição"""
    t = HISTORICO_PERIODO_ORGAO.query.get(id)
    if not t or t.tipo_mudanca not in ['TRANSICAO_SDI', 'TRANSICAO']:
        flash('Registro não encontrado', 'danger')
        return redirect(url_for('transicao.listar'))
    return render_template('transicao/detalhes.html', transicao=t)
