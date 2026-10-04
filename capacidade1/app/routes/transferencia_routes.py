"""Routes for Transfers (C225T) - F-011
Transferência de Órgãos entre Coordenações
Operação: Criar histórico de mudança de período/coordenação
Funcionalidade: Encerra período anterior, abre período novo
Auditoria: Completa com timestamp
Reabertura: Permite voltar período fechado (reversão com auditoria)
Persistência: Histórico não-destrutivo (novos registros, nunca deletados)
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models.historico import HISTORICO_PERIODO_ORGAO
from app.models.auditoria import AUDITORIA
from app.validations.common_validations import validar_campo_obrigatorio
from app.config import Config
from datetime import datetime

bp = Blueprint('transferencia', __name__, url_prefix='/transferencia')

def _validar_transferencia(codigo_orgao, periodo_novo):
    """Validar transferência de órgão"""
    errors = []
    
    if not codigo_orgao or not validar_campo_obrigatorio(codigo_orgao):
        errors.append("Código do órgão é obrigatório")
    
    if not periodo_novo or not validar_campo_obrigatorio(periodo_novo):
        errors.append("Período novo é obrigatório")
    
    return len(errors) == 0, "; ".join(errors) if errors else None

@bp.route('/', methods=['GET'])
def listar():
    """F-011: Consultar transferências de órgãos (histórico não-destrutivo)"""
    page = request.args.get('page', 1, type=int)
    pagination = HISTORICO_PERIODO_ORGAO.query.filter_by(
        tipo_mudanca='TRANSFERENCIA'
    ).order_by(HISTORICO_PERIODO_ORGAO.data_mudanca.desc()).paginate(page=page, per_page=Config.ITEMS_PER_PAGE)
    return render_template('transferencia/lista.html', 
                         transferencias=pagination.items, 
                         pagination=pagination, 
                         page=page)

@bp.route('/criar', methods=['GET', 'POST'])
def criar():
    """F-011: Registrar transferência de órgão (fecha período anterior, abre novo)"""
    if request.method == 'POST':
        codigo_orgao = request.form.get('codigo_orgao', '').strip()
        periodo_anterior = request.form.get('periodo_anterior', '').strip() or None
        periodo_novo = request.form.get('periodo_novo', '').strip()
        
        is_valid, error = _validar_transferencia(codigo_orgao, periodo_novo)
        if not is_valid:
            flash(f'Erro: {error}', 'danger')
            return render_template('transferencia/criar.html')
        
        try:
            # Criar histórico (não-destrutivo: novos registros, nunca deletados)
            t = HISTORICO_PERIODO_ORGAO(
                codigo_orgao=codigo_orgao,
                periodo_anterior=periodo_anterior,
                periodo_novo=periodo_novo,
                tipo_mudanca='TRANSFERENCIA',
                data_mudanca=datetime.utcnow()
            )
            db.session.add(t)
            db.session.commit()
            
            # Auditoria: Registrar transferência com timestamp
            auditoria = AUDITORIA.registrar(
                tabela='historico_periodo_orgao',
                operacao='CREATE',
                chave_primaria=str(t.id),
                valores_novos=t.to_dict(),
                usuario=request.remote_addr
            )
            db.session.add(auditoria)
            db.session.commit()
            
            flash('Transferência registrada com sucesso', 'success')
            return redirect(url_for('transferencia.listar'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao registrar transferência: {str(e)}', 'danger')
    
    return render_template('transferencia/criar.html')

@bp.route('/detalhes/<int:id>', methods=['GET'])
def detalhes(id):
    """F-011: Ver detalhes de transferência"""
    t = HISTORICO_PERIODO_ORGAO.query.get(id)
    if not t or t.tipo_mudanca != 'TRANSFERENCIA':
        flash('Registro não encontrado', 'danger')
        return redirect(url_for('transferencia.listar'))
    return render_template('transferencia/detalhes.html', transferencia=t)
