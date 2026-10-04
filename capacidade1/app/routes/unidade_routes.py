"""Routes for Budgetary Units (C025T) - F-002
Manter Unidades Orçamentárias
Operações: CON, I, A, E
Validações: RN-01 (8d código), RN-02 (desc 40c), RN-03 (duplicação), 
            RN-14 (guarda por grupos/contratos)
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app import db
from app.models.unidade import UNIDADE_ORCAMENTARIA
from app.models.auditoria import AUDITORIA
from app.models.grupo import GRUPO
from app.validations.common_validations import validar_campo_obrigatorio, validar_numerico
from app.config import Config

bp = Blueprint('unidade', __name__, url_prefix='/unidade')

def _validar_unidade(codigo_unidade, descricao):
    """RN-01, RN-02, RN-03: Validar unidade orçamentária"""
    errors = []
    
    # RN-01: Código 8 dígitos numérico
    if not codigo_unidade or not validar_numerico(codigo_unidade):
        errors.append("Código deve conter apenas números")
    elif len(codigo_unidade) != 8:
        errors.append("Código deve ter exatamente 8 dígitos")
    
    # RN-02: Descrição obrigatória (40 caracteres max)
    if not descricao or not validar_campo_obrigatorio(descricao):
        errors.append("Descrição é obrigatória")
    elif len(descricao) > 40:
        errors.append("Descrição não pode exceder 40 caracteres")
    
    return len(errors) == 0, "; ".join(errors) if errors else None

def _verificar_grupos_contratos_existem(codigo_unidade):
    """RN-14: Verificar se grupos ou contratos dependem desta unidade (guarda)"""
    grupos_existem = GRUPO.query.filter_by(codigo_unidade=codigo_unidade).first() is not None
    # TODO: Verificar contratos quando modelo disponível
    return grupos_existem

@bp.route('/', methods=['GET'])
def listar():
    """F-002: Consultar todas as unidades com paginação (15 itens)"""
    page = request.args.get('page', 1, type=int)
    per_page = Config.ITEMS_PER_PAGE
    
    pagination = UNIDADE_ORCAMENTARIA.query.order_by(UNIDADE_ORCAMENTARIA.codigo_unidade).paginate(page=page, per_page=per_page)
    unidades = pagination.items
    
    return render_template('unidade/lista.html',
                          unidades=unidades,
                          pagination=pagination,
                          page=page)

@bp.route('/criar', methods=['GET', 'POST'])
def criar():
    """F-002: Criar nova unidade orçamentária"""
    if request.method == 'POST':
        codigo_unidade = request.form.get('codigo_unidade', '').strip()
        descricao = request.form.get('descricao', '').strip()
        
        is_valid, error_message = _validar_unidade(codigo_unidade, descricao)
        if not is_valid:
            flash(f'Erro: {error_message}', 'danger')
            return render_template('unidade/criar.html')
        
        # RN-03: Não permitir duplicação de código
        unidade_existente = UNIDADE_ORCAMENTARIA.query.filter_by(
            codigo_unidade=codigo_unidade
        ).first()
        if unidade_existente:
            flash(f'Unidade já existe', 'danger')
            return render_template('unidade/criar.html')
        
        nova_unidade = UNIDADE_ORCAMENTARIA(
            codigo_unidade=codigo_unidade,
            descricao=descricao
        )
        
        try:
            db.session.add(nova_unidade)
            db.session.commit()
            
            # Auditoria: Registrar criação com valores novos
            auditoria = AUDITORIA.registrar(
                tabela='unidade_orcamentaria',
                operacao='CREATE',
                chave_primaria=codigo_unidade,
                valores_novos=nova_unidade.to_dict(),
                usuario=request.remote_addr
            )
            db.session.add(auditoria)
            db.session.commit()
            
            flash('Unidade criada com sucesso', 'success')
            return redirect(url_for('unidade.listar'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao criar unidade: {str(e)}', 'danger')
    
    return render_template('unidade/criar.html')

@bp.route('/editar/<codigo_unidade>', methods=['GET', 'POST'])
def editar(codigo_unidade):
    """F-002: Editar unidade orçamentária (valores prior/post)"""
    unidade = UNIDADE_ORCAMENTARIA.query.get(codigo_unidade)
    
    if not unidade:
        flash('Unidade não encontrada', 'danger')
        return redirect(url_for('unidade.listar'))
    
    if request.method == 'POST':
        descricao = request.form.get('descricao', '').strip()
        
        is_valid, error_message = _validar_unidade(codigo_unidade, descricao)
        if not is_valid:
            flash(f'Erro: {error_message}', 'danger')
            return render_template('unidade/editar.html', unidade=unidade)
        
        valores_anteriores = unidade.to_dict()
        unidade.descricao = descricao
        
        try:
            db.session.commit()
            
            # Auditoria: Registrar alteração com valores prior/post
            auditoria = AUDITORIA.registrar(
                tabela='unidade_orcamentaria',
                operacao='UPDATE',
                chave_primaria=codigo_unidade,
                valores_anteriores=valores_anteriores,
                valores_novos=unidade.to_dict(),
                usuario=request.remote_addr
            )
            db.session.add(auditoria)
            db.session.commit()
            
            flash('Unidade atualizada com sucesso', 'success')
            return redirect(url_for('unidade.listar'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar unidade: {str(e)}', 'danger')
    
    return render_template('unidade/editar.html', unidade=unidade)

@bp.route('/deletar/<codigo_unidade>', methods=['POST'])
def deletar(codigo_unidade):
    """F-002: Deletar unidade (RN-14: Guarda - não deletar se grupos/contratos existem)"""
    unidade = UNIDADE_ORCAMENTARIA.query.get(codigo_unidade)
    
    if not unidade:
        flash('Unidade não encontrada', 'danger')
        return redirect(url_for('unidade.listar'))
    
    # RN-14: Verificar se grupos ou contratos dependem desta unidade
    if _verificar_grupos_contratos_existem(codigo_unidade):
        flash('Não é possível deletar unidade pois existem grupos ou contratos vinculados', 'danger')
        return redirect(url_for('unidade.listar'))
    
    try:
        valores = unidade.to_dict()
        db.session.delete(unidade)
        db.session.commit()
        
        # Auditoria: Registrar deleção
        auditoria = AUDITORIA.registrar(
            tabela='unidade_orcamentaria',
            operacao='DELETE',
            chave_primaria=codigo_unidade,
            valores_anteriores=valores,
            usuario=request.remote_addr
        )
        db.session.add(auditoria)
        db.session.commit()
        
        flash('Unidade deletada com sucesso', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao deletar unidade: {str(e)}', 'danger')
    
    return redirect(url_for('unidade.listar'))

@bp.route('/api/<codigo_unidade>', methods=['GET'])
def get_json(codigo_unidade):
    """Get unit data as JSON"""
    unidade = UNIDADE_ORCAMENTARIA.query.get(codigo_unidade)
    if not unidade:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(unidade.to_dict())
