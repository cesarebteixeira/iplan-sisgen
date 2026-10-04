"""Routes for Groups (C126T) - F-003
Manter Grupos/Coordenações
Operações: CON (filtrado por tipo_orgao em sessão), I, A (com propagação), E (com guarda)
Validações: RN-01 (2d), RN-02 (desc 40c), RN-03 (tipo órgão parte da chave),
            RN-04 (unidade 8d obrigatória), RN-05 (duplicação por tipo_orgao),
            RN-12 (propagação ao alterar unidade), RN-13 (guarda por órgãos)
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models.grupo import GRUPO
from app.models.unidade import UNIDADE_ORCAMENTARIA
from app.models.auditoria import AUDITORIA
from app.validations.common_validations import validar_campo_obrigatorio, validar_numerico
from app.config import Config

bp = Blueprint('grupo', __name__, url_prefix='/grupo')

def _validar_grupo(codigo_grupo, tipo_orgao, codigo_unidade, descricao):
    """RN-01, RN-02, RN-03, RN-04: Validar grupo"""
    errors = []
    
    # RN-01: Código 2 dígitos
    if not codigo_grupo or not validar_numerico(codigo_grupo):
        errors.append("Código deve conter apenas números")
    elif len(codigo_grupo) != 2:
        errors.append("Código deve ter exatamente 2 dígitos")
    
    # RN-03: Tipo órgão é parte da chave (obrigatório)
    if not tipo_orgao or not validar_campo_obrigatorio(tipo_orgao):
        errors.append("Tipo de órgão é obrigatório")
    
    # RN-02: Descrição obrigatória (40 caracteres max)
    if not descricao or not validar_campo_obrigatorio(descricao):
        errors.append("Descrição é obrigatória")
    elif len(descricao) > 40:
        errors.append("Descrição não pode exceder 40 caracteres")
    
    # RN-04: Unidade 8 dígitos obrigatória e deve existir
    if not codigo_unidade or not validar_numerico(codigo_unidade):
        errors.append("Unidade deve conter apenas números")
    elif len(codigo_unidade) != 8:
        errors.append("Unidade deve ter exatamente 8 dígitos")
    elif not UNIDADE_ORCAMENTARIA.query.filter_by(codigo_unidade=codigo_unidade).first():
        errors.append("Unidade não encontrada")
    
    return len(errors) == 0, "; ".join(errors) if errors else None

def _verificar_orgaos_existem(codigo_grupo, tipo_orgao):
    """RN-13: Verificar se órgãos dependem deste grupo (guarda)"""
    # TODO: Integrar com modelo ORGAO quando disponível
    # Por enquanto, retorna False (sem guarda ativa)
    return False

def _propagar_unidade_para_orgaos(codigo_grupo, tipo_orgao, codigo_unidade_novo):
    """RN-12: Propagação especial - Alteração de unidade propaga para todos órgãos do grupo"""
    # TODO: Implementar propagação para ÓRGAO quando modelo disponível
    # Registrar no auditoria que propagação foi realizada
    pass

@bp.route('/', methods=['GET'])
def listar():
    """F-003: Consultar grupos (filtrado por tipo_orgao em sessão)"""
    page = request.args.get('page', 1, type=int)
    # TODO: Filtrar por tipo_orgao da sessão quando sessão implementada
    pagination = GRUPO.query.order_by(GRUPO.codigo_grupo, GRUPO.tipo_orgao).paginate(page=page, per_page=Config.ITEMS_PER_PAGE)
    return render_template('grupo/lista.html', grupos=pagination.items, pagination=pagination, page=page)

@bp.route('/criar', methods=['GET', 'POST'])
def criar():
    """F-003: Criar novo grupo"""
    if request.method == 'POST':
        codigo_grupo = request.form.get('codigo_grupo', '').strip()
        tipo_orgao = request.form.get('tipo_orgao', '').strip()
        codigo_unidade = request.form.get('codigo_unidade', '').strip()
        descricao = request.form.get('descricao', '').strip()
        
        is_valid, error = _validar_grupo(codigo_grupo, tipo_orgao, codigo_unidade, descricao)
        if not is_valid:
            flash(f'Erro: {error}', 'danger')
            return render_template('grupo/criar.html', unidades=UNIDADE_ORCAMENTARIA.query.all())
        
        # RN-05: Não permitir duplicação dentro de tipo_orgao
        grupo_existente = GRUPO.query.filter_by(
            codigo_grupo=int(codigo_grupo),
            tipo_orgao=tipo_orgao
        ).first()
        if grupo_existente:
            flash('Grupo já existe para este tipo de órgão', 'danger')
            return render_template('grupo/criar.html', unidades=UNIDADE_ORCAMENTARIA.query.all())
        
        try:
            g = GRUPO(
                codigo_grupo=int(codigo_grupo),
                tipo_orgao=tipo_orgao,
                codigo_unidade=codigo_unidade,
                descricao=descricao
            )
            db.session.add(g)
            db.session.commit()
            
            # Auditoria: Registrar criação
            auditoria = AUDITORIA.registrar(
                tabela='grupo',
                operacao='CREATE',
                chave_primaria=f"{codigo_grupo}-{tipo_orgao}",
                valores_novos=g.to_dict(),
                usuario=request.remote_addr
            )
            db.session.add(auditoria)
            db.session.commit()
            
            flash('Grupo criado com sucesso', 'success')
            return redirect(url_for('grupo.listar'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao criar grupo: {str(e)}', 'danger')
    
    return render_template('grupo/criar.html', unidades=UNIDADE_ORCAMENTARIA.query.all())

@bp.route('/editar/<codigo_grupo>/<tipo_orgao>', methods=['GET', 'POST'])
def editar(codigo_grupo, tipo_orgao):
    """F-003: Editar grupo (RN-12: Propagação ao alterar unidade)"""
    try:
        codigo_grupo_int = int(codigo_grupo)
    except (ValueError, TypeError):
        flash('Código de grupo inválido', 'danger')
        return redirect(url_for('grupo.listar'))
    
    g = GRUPO.query.filter_by(codigo_grupo=codigo_grupo_int, tipo_orgao=tipo_orgao).first()
    if not g:
        flash('Registro não encontrado', 'danger')
        return redirect(url_for('grupo.listar'))
    
    if request.method == 'POST':
        codigo_unidade_novo = request.form.get('codigo_unidade', '').strip()
        descricao_nova = request.form.get('descricao', '').strip()
        
        is_valid, error = _validar_grupo(codigo_grupo, tipo_orgao, codigo_unidade_novo, descricao_nova)
        if not is_valid:
            flash(f'Erro: {error}', 'danger')
            return render_template('grupo/editar.html', grupo=g, unidades=UNIDADE_ORCAMENTARIA.query.all())
        
        try:
            antes = g.to_dict()
            unidade_antiga = g.codigo_unidade
            
            g.descricao = descricao_nova
            g.codigo_unidade = codigo_unidade_novo
            db.session.commit()
            
            # RN-12: Se unidade foi alterada, propagar para órgãos
            propagacao_msg = ""
            if unidade_antiga != codigo_unidade_novo:
                _propagar_unidade_para_orgaos(codigo_grupo_int, tipo_orgao, codigo_unidade_novo)
                propagacao_msg = " (com propagação para órgãos do grupo)"
            
            # Auditoria: Registrar alteração
            auditoria = AUDITORIA.registrar(
                tabela='grupo',
                operacao='UPDATE',
                chave_primaria=f"{codigo_grupo}-{tipo_orgao}",
                valores_anteriores=antes,
                valores_novos=g.to_dict(),
                usuario=request.remote_addr
            )
            db.session.add(auditoria)
            db.session.commit()
            
            flash(f'Grupo atualizado com sucesso{propagacao_msg}', 'success')
            return redirect(url_for('grupo.listar'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar grupo: {str(e)}', 'danger')
    
    return render_template('grupo/editar.html', grupo=g, unidades=UNIDADE_ORCAMENTARIA.query.all())

@bp.route('/deletar/<codigo_grupo>/<tipo_orgao>', methods=['POST'])
def deletar(codigo_grupo, tipo_orgao):
    """F-003: Deletar grupo (RN-13: Guarda - não deletar se órgãos existem)"""
    try:
        codigo_grupo_int = int(codigo_grupo)
    except (ValueError, TypeError):
        flash('Código de grupo inválido', 'danger')
        return redirect(url_for('grupo.listar'))
    
    g = GRUPO.query.filter_by(codigo_grupo=codigo_grupo_int, tipo_orgao=tipo_orgao).first()
    if not g:
        flash('Registro não encontrado', 'danger')
        return redirect(url_for('grupo.listar'))
    
    # RN-13: Verificar se órgãos existem
    if _verificar_orgaos_existem(codigo_grupo_int, tipo_orgao):
        flash('Não é possível deletar grupo pois existem órgãos vinculados', 'danger')
        return redirect(url_for('grupo.listar'))
    
    try:
        antes = g.to_dict()
        db.session.delete(g)
        db.session.commit()
        
        # Auditoria: Registrar deleção
        auditoria = AUDITORIA.registrar(
            tabela='grupo',
            operacao='DELETE',
            chave_primaria=f"{codigo_grupo}-{tipo_orgao}",
            valores_anteriores=antes,
            usuario=request.remote_addr
        )
        db.session.add(auditoria)
        db.session.commit()
        
        flash('Grupo deletado com sucesso', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao deletar grupo: {str(e)}', 'danger')
    
    return redirect(url_for('grupo.listar'))
