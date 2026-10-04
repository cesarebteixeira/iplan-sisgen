"""Routes for Process Types (C162T) - F-006
Manter Tipos de Processo
Operações: CON (filtrado por tipo_orgao em sessão), I, A
Validações: RN-01 (2d código), RN-02 (tipo_orgao parte da chave),
            RN-03 (desc 40c), RN-04 (duplicação dentro tipo_orgao)
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models.tipo_processo import TIPO_PROCESSO
from app.models.auditoria import AUDITORIA
from app.validations.common_validations import validar_campo_obrigatorio, validar_numerico
from app.config import Config

bp = Blueprint('tipo_processo', __name__, url_prefix='/tipo-processo')

def _validar_tipo_processo(codigo_tipo, descricao):
    """RN-01, RN-02, RN-03: Validar tipo de processo"""
    errors = []
    
    # RN-01: Código 2 dígitos
    if not codigo_tipo or not validar_numerico(codigo_tipo):
        errors.append("Código deve conter apenas números")
    elif len(codigo_tipo) != 2:
        errors.append("Código deve ter exatamente 2 dígitos")
    
    # RN-03: Descrição obrigatória (40 caracteres max)
    if not descricao or not validar_campo_obrigatorio(descricao):
        errors.append("Descrição é obrigatória")
    elif len(descricao) > 40:
        errors.append("Descrição não pode exceder 40 caracteres")
    
    return len(errors) == 0, "; ".join(errors) if errors else None

@bp.route('/', methods=['GET'])
def listar():
    """F-006: Consultar tipos de processo (filtrado por tipo_orgao em sessão)"""
    page = request.args.get('page', 1, type=int)
    # TODO: Filtrar por tipo_orgao da sessão quando sessão implementada
    pagination = TIPO_PROCESSO.query.order_by(TIPO_PROCESSO.codigo_tipo).paginate(page=page, per_page=Config.ITEMS_PER_PAGE)
    return render_template('tipo_processo/lista.html', 
                         tipos=pagination.items, 
                         pagination=pagination, 
                         page=page)

@bp.route('/criar', methods=['GET', 'POST'])
def criar():
    """F-006: Criar novo tipo de processo"""
    if request.method == 'POST':
        codigo_tipo = request.form.get('codigo_tipo', '').strip()
        descricao = request.form.get('descricao', '').strip()
        
        is_valid, error = _validar_tipo_processo(codigo_tipo, descricao)
        if not is_valid:
            flash(f'Erro: {error}', 'danger')
            return render_template('tipo_processo/criar.html')
        
        # RN-04: Não permitir duplicação de código
        tipo_existente = TIPO_PROCESSO.query.filter_by(codigo_tipo=int(codigo_tipo)).first()
        if tipo_existente:
            flash('Tipo de processo já existe', 'danger')
            return render_template('tipo_processo/criar.html')
        
        try:
            t = TIPO_PROCESSO(codigo_tipo=int(codigo_tipo), descricao=descricao)
            db.session.add(t)
            db.session.commit()
            
            # Auditoria: Registrar criação
            auditoria = AUDITORIA.registrar(
                tabela='tipo_processo',
                operacao='CREATE',
                chave_primaria=str(codigo_tipo),
                valores_novos=t.to_dict(),
                usuario=request.remote_addr
            )
            db.session.add(auditoria)
            db.session.commit()
            
            flash('Tipo de Processo criado com sucesso', 'success')
            return redirect(url_for('tipo_processo.listar'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao criar tipo de processo: {str(e)}', 'danger')
    
    return render_template('tipo_processo/criar.html')

@bp.route('/editar/<codigo_tipo>', methods=['GET', 'POST'])
def editar(codigo_tipo):
    """F-006: Editar tipo de processo"""
    try:
        codigo_tipo_int = int(codigo_tipo)
    except (ValueError, TypeError):
        flash('Código inválido', 'danger')
        return redirect(url_for('tipo_processo.listar'))
    
    t = TIPO_PROCESSO.query.get(codigo_tipo_int)
    if not t:
        flash('Registro não encontrado', 'danger')
        return redirect(url_for('tipo_processo.listar'))
    
    if request.method == 'POST':
        descricao = request.form.get('descricao', '').strip()
        
        is_valid, error = _validar_tipo_processo(codigo_tipo, descricao)
        if not is_valid:
            flash(f'Erro: {error}', 'danger')
            return render_template('tipo_processo/editar.html', tipo=t)
        
        try:
            antes = t.to_dict()
            t.descricao = descricao
            db.session.commit()
            
            # Auditoria: Registrar alteração
            auditoria = AUDITORIA.registrar(
                tabela='tipo_processo',
                operacao='UPDATE',
                chave_primaria=str(codigo_tipo_int),
                valores_anteriores=antes,
                valores_novos=t.to_dict(),
                usuario=request.remote_addr
            )
            db.session.add(auditoria)
            db.session.commit()
            
            flash('Tipo de Processo atualizado com sucesso', 'success')
            return redirect(url_for('tipo_processo.listar'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar tipo de processo: {str(e)}', 'danger')
    
    return render_template('tipo_processo/editar.html', tipo=t)
