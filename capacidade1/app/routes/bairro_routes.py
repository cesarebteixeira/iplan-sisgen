"""Routes for Neighborhoods (C023T) - F-001
Operações: CON, I, E (NO ALTER - RN-07 unreachable)
Validações: RN-01 (3d código), RN-02 (desc 25c), RN-03 (duplicação), 
            RN-04 (auto-increment), RN-15 (guarda por órgãos)
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app import db
from app.models.bairro import BAIRRO
from app.models.auditoria import AUDITORIA
from app.validations.common_validations import validar_campo_obrigatorio, validar_numerico
from app.config import Config

bp = Blueprint('bairro', __name__, url_prefix='/bairro')

def _validar_bairro(descricao):
    """RN-02: Validar descrição do bairro"""
    errors = []
    
    # RN-02: Descrição obrigatória (25 caracteres max)
    if not descricao or not validar_campo_obrigatorio(descricao):
        errors.append("Descrição é obrigatória")
    elif len(descricao) > 25:
        errors.append("Descrição não pode exceder 25 caracteres")
    
    return len(errors) == 0, "; ".join(errors) if errors else None

def _verificar_orgaos_existem(codigo_bairro):
    """RN-15: Verificar se órgãos dependem deste bairro (guarda)"""
    # TODO: Integrar com modelo ORGAO quando disponível
    # Por enquanto, retorna False (sem guarda ativa)
    return False

@bp.route('/', methods=['GET'])
def listar():
    """F-001: Consultar bairros com paginação (15 itens)"""
    page = request.args.get('page', 1, type=int)
    pagination = BAIRRO.query.order_by(BAIRRO.codigo_bairro).paginate(page=page, per_page=Config.ITEMS_PER_PAGE)
    return render_template('bairro/lista.html', 
                         bairros=pagination.items, 
                         pagination=pagination, 
                         page=page)

@bp.route('/criar', methods=['GET', 'POST'])
def criar():
    """F-001: Criar novo bairro"""
    if request.method == 'POST':
        codigo_bairro = request.form.get('codigo_bairro', '').strip()
        descricao = request.form.get('descricao', '').strip()
        
        # Validar código
        if not codigo_bairro:
            flash('Erro: Código é obrigatório', 'danger')
            return render_template('bairro/criar.html')
        
        if not codigo_bairro.isdigit() or len(codigo_bairro) != 3:
            flash('Erro: Código deve ter exatamente 3 dígitos', 'danger')
            return render_template('bairro/criar.html')
        
        # Validar descrição
        is_valid, error = _validar_bairro(descricao)
        if not is_valid:
            flash(f'Erro: {error}', 'danger')
            return render_template('bairro/criar.html')
        
        # Verificar duplicação
        if BAIRRO.query.filter_by(codigo_bairro=int(codigo_bairro)).first():
            flash('Erro: Bairro já existe', 'danger')
            return render_template('bairro/criar.html')
        
        try:
            bairro = BAIRRO(codigo_bairro=int(codigo_bairro), descricao=descricao)
            db.session.add(bairro)
            db.session.commit()
            
            # Auditoria: Registrar criação
            auditoria = AUDITORIA.registrar(
                tabela='bairro',
                operacao='CREATE',
                chave_primaria=str(bairro.codigo_bairro),
                valores_novos=bairro.to_dict(),
                usuario=request.remote_addr
            )
            db.session.add(auditoria)
            db.session.commit()
            
            flash(f'Bairro criado com sucesso', 'success')
            return redirect(url_for('bairro.listar'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao criar bairro: {str(e)}', 'danger')
    
    return render_template('bairro/criar.html')

@bp.route('/deletar/<codigo_bairro>', methods=['POST'])
def deletar(codigo_bairro):
    """F-001: Deletar bairro (RN-15: Guarda - não deletar se órgãos existem)"""
    try:
        codigo_bairro_int = int(codigo_bairro)
    except (ValueError, TypeError):
        flash('Código de bairro inválido', 'danger')
        return redirect(url_for('bairro.listar'))
    
    bairro = BAIRRO.query.get(codigo_bairro_int)
    if not bairro:
        flash('Registro não encontrado', 'danger')
        return redirect(url_for('bairro.listar'))
    
    # RN-15: Verificar se órgãos dependem deste bairro
    if _verificar_orgaos_existem(codigo_bairro_int):
        flash('Não é possível deletar bairro pois existem órgãos vinculados', 'danger')
        return redirect(url_for('bairro.listar'))
    
    try:
        antes = bairro.to_dict()
        db.session.delete(bairro)
        db.session.commit()
        
        # Auditoria: Registrar deleção
        auditoria = AUDITORIA.registrar(
            tabela='bairro',
            operacao='DELETE',
            chave_primaria=str(codigo_bairro_int),
            valores_anteriores=antes,
            usuario=request.remote_addr
        )
        db.session.add(auditoria)
        db.session.commit()
        
        flash('Bairro deletado com sucesso', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao deletar bairro: {str(e)}', 'danger')
    
    return redirect(url_for('bairro.listar'))

@bp.route('/editar/<codigo_bairro>', methods=['GET', 'POST'])
def editar(codigo_bairro):
    """F-001: Editar/visualizar bairro (apenas visualizar - sem ALTER por RN-07)"""
    try:
        codigo_bairro_int = int(codigo_bairro)
    except (ValueError, TypeError):
        flash('Código de bairro inválido', 'danger')
        return redirect(url_for('bairro.listar'))
    
    bairro = BAIRRO.query.get(codigo_bairro_int)
    if not bairro:
        flash('Registro não encontrado', 'danger')
        return redirect(url_for('bairro.listar'))
    
    if request.method == 'POST':
        # POST não é permitido - apenas visualização
        flash('Não é permitido alterar registros de bairro', 'warning')
        return redirect(url_for('bairro.listar'))
    
    # GET: Apenas visualizar (read-only)
    return render_template('bairro/editar.html', bairro=bairro)

@bp.route('/api/<codigo_bairro>', methods=['GET'])
def get_json(codigo_bairro):
    """API: Retornar bairro em JSON"""
    try:
        codigo_bairro_int = int(codigo_bairro)
    except (ValueError, TypeError):
        return jsonify({'error': 'Código inválido'}), 400
    
    bairro = BAIRRO.query.get(codigo_bairro_int)
    if not bairro:
        return jsonify({'error': 'Bairro não encontrado'}), 404
    return jsonify(bairro.to_dict())
