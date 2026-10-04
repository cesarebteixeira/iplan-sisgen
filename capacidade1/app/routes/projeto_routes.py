"""Routes for Projects (C205T) - F-009
Manter Projetos da Secretaria
Operações: CON, I, A, E (com guarda)
Validações: RN-01 (2d código), RN-02 (secretaria parte da chave),
            RN-03 (desc 40c obrigatória), RN-04 (capacidade 999 por secretaria, 0=blank),
            RN-05 (duplicação dentro secretaria), RN-14 (guarda por vínculos órgão-projeto)
Escopo: Por secretaria
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models.projeto import PROJETO
from app.models.vinculo import VINCULO_ORGAO_PROJETO
from app.models.auditoria import AUDITORIA
from app.validations.common_validations import validar_campo_obrigatorio, validar_numerico
from app.config import Config

bp = Blueprint('projeto', __name__, url_prefix='/projeto')

def _validar_projeto(codigo_projeto, secretaria, descricao, capacidade=None):
    """RN-01, RN-02, RN-03, RN-04: Validar projeto"""
    errors = []
    
    # RN-01: Código 2 dígitos
    if not codigo_projeto or not validar_numerico(codigo_projeto):
        errors.append("Código deve conter apenas números")
    elif len(codigo_projeto) != 2:
        errors.append("Código deve ter exatamente 2 dígitos")
    
    # RN-02: Secretaria é parte da chave (obrigatória)
    if not secretaria or not validar_campo_obrigatorio(secretaria):
        errors.append("Secretaria é obrigatória")
    
    # RN-03: Descrição obrigatória (40 caracteres max)
    if not descricao or not validar_campo_obrigatorio(descricao):
        errors.append("Descrição é obrigatória")
    elif len(descricao) > 40:
        errors.append("Descrição não pode exceder 40 caracteres")
    
    # RN-04: Capacidade 999 por secretaria (0 = blank/vazio)
    if capacidade is not None:
        try:
            cap = int(capacidade)
            if cap < 0 or cap > 999:
                errors.append("Capacidade deve ser entre 0 e 999")
        except (ValueError, TypeError):
            if capacidade != '':
                errors.append("Capacidade deve ser um número ou vazio")
    
    return len(errors) == 0, "; ".join(errors) if errors else None

def _verificar_vinculos_existem(codigo_projeto, secretaria):
    """RN-14: Verificar se vínculos órgão-projeto existem (guarda)"""
    vinculos_existem = VINCULO_ORGAO_PROJETO.query.filter_by(codigo_projeto=int(codigo_projeto)).first() is not None
    return vinculos_existem

@bp.route('/', methods=['GET'])
def listar():
    """F-009: Consultar projetos (filtrado por secretaria em sessão)"""
    page = request.args.get('page', 1, type=int)
    # TODO: Filtrar por secretaria da sessão quando sessão implementada
    pagination = PROJETO.query.order_by(PROJETO.codigo_projeto, PROJETO.secretaria).paginate(page=page, per_page=Config.ITEMS_PER_PAGE)
    return render_template('projeto/lista.html', 
                         projetos=pagination.items, 
                         pagination=pagination, 
                         page=page)

@bp.route('/criar', methods=['GET', 'POST'])
def criar():
    """F-009: Criar novo projeto"""
    if request.method == 'POST':
        codigo_projeto = request.form.get('codigo_projeto', '').strip()
        secretaria = request.form.get('secretaria', '').strip()
        descricao = request.form.get('descricao', '').strip()
        capacidade = request.form.get('capacidade', '').strip() or '0'
        
        is_valid, error = _validar_projeto(codigo_projeto, secretaria, descricao, capacidade)
        if not is_valid:
            flash(f'Erro: {error}', 'danger')
            return render_template('projeto/criar.html')
        
        # RN-05: Não permitir duplicação dentro de secretaria
        projeto_existente = PROJETO.query.filter_by(
            codigo_projeto=int(codigo_projeto),
            secretaria=secretaria
        ).first()
        if projeto_existente:
            flash('Projeto já existe para esta secretaria', 'danger')
            return render_template('projeto/criar.html')
        
        try:
            p = PROJETO(
                codigo_projeto=int(codigo_projeto),
                secretaria=secretaria,
                descricao=descricao,
                capacidade=int(capacidade) if capacidade else 0
            )
            db.session.add(p)
            db.session.commit()
            
            # Auditoria: Registrar criação
            auditoria = AUDITORIA.registrar(
                tabela='projeto',
                operacao='CREATE',
                chave_primaria=f"{codigo_projeto}-{secretaria}",
                valores_novos=p.to_dict(),
                usuario=request.remote_addr
            )
            db.session.add(auditoria)
            db.session.commit()
            
            flash('Projeto criado com sucesso', 'success')
            return redirect(url_for('projeto.listar'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao criar projeto: {str(e)}', 'danger')
    
    return render_template('projeto/criar.html')

@bp.route('/editar/<codigo_projeto>/<secretaria>', methods=['GET', 'POST'])
def editar(codigo_projeto, secretaria):
    """F-009: Editar projeto"""
    try:
        codigo_projeto_int = int(codigo_projeto)
    except (ValueError, TypeError):
        flash('Código de projeto inválido', 'danger')
        return redirect(url_for('projeto.listar'))
    
    p = PROJETO.query.filter_by(codigo_projeto=codigo_projeto_int, secretaria=secretaria).first()
    if not p:
        flash('Registro não encontrado', 'danger')
        return redirect(url_for('projeto.listar'))
    
    if request.method == 'POST':
        descricao = request.form.get('descricao', '').strip()
        capacidade = request.form.get('capacidade', '').strip() or '0'
        
        is_valid, error = _validar_projeto(codigo_projeto, secretaria, descricao, capacidade)
        if not is_valid:
            flash(f'Erro: {error}', 'danger')
            return render_template('projeto/editar.html', projeto=p)
        
        try:
            antes = p.to_dict()
            p.descricao = descricao
            p.capacidade = int(capacidade) if capacidade else 0
            db.session.commit()
            
            # Auditoria: Registrar alteração
            auditoria = AUDITORIA.registrar(
                tabela='projeto',
                operacao='UPDATE',
                chave_primaria=f"{codigo_projeto}-{secretaria}",
                valores_anteriores=antes,
                valores_novos=p.to_dict(),
                usuario=request.remote_addr
            )
            db.session.add(auditoria)
            db.session.commit()
            
            flash('Projeto atualizado com sucesso', 'success')
            return redirect(url_for('projeto.listar'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar projeto: {str(e)}', 'danger')
    
    return render_template('projeto/editar.html', projeto=p)

@bp.route('/deletar/<codigo_projeto>/<secretaria>', methods=['POST'])
def deletar(codigo_projeto, secretaria):
    """F-009: Deletar projeto (RN-14: Guarda - não deletar se vínculos existem)"""
    try:
        codigo_projeto_int = int(codigo_projeto)
    except (ValueError, TypeError):
        flash('Código de projeto inválido', 'danger')
        return redirect(url_for('projeto.listar'))
    
    p = PROJETO.query.filter_by(codigo_projeto=codigo_projeto_int, secretaria=secretaria).first()
    if not p:
        flash('Registro não encontrado', 'danger')
        return redirect(url_for('projeto.listar'))
    
    # RN-14: Verificar se vínculos órgão-projeto existem
    if _verificar_vinculos_existem(codigo_projeto_int, secretaria):
        flash('Não é possível deletar projeto pois existem vínculos órgão-projeto', 'danger')
        return redirect(url_for('projeto.listar'))
    
    try:
        antes = p.to_dict()
        db.session.delete(p)
        db.session.commit()
        
        # Auditoria: Registrar deleção
        auditoria = AUDITORIA.registrar(
            tabela='projeto',
            operacao='DELETE',
            chave_primaria=f"{codigo_projeto}-{secretaria}",
            valores_anteriores=antes,
            usuario=request.remote_addr
        )
        db.session.add(auditoria)
        db.session.commit()
        
        flash('Projeto deletado com sucesso', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao deletar projeto: {str(e)}', 'danger')
    
    return redirect(url_for('projeto.listar'))
