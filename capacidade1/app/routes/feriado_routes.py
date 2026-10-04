"""Routes for Holidays (C192T/C806T) - F-008
Manter Feriados do Órgão
Operações: CON, I, A, E
Validações: RN-01 (data DDMMYYYY válida, 1994-2099), RN-02 (código_orgao parte da chave),
            RN-03 (tipo_orgao parte da chave), RN-04 (desc 40c obrigatória),
            RN-05 (creche opcional S/N), RN-06 (recesso_literal = "RECESSO" ou "RECESSO ESCOLAR" ou null),
            RN-07 (validar data está no calendário)
Escopo: Por órgão
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models.feriado import FERIADO_ORGAO
from app.models.auditoria import AUDITORIA
from app.validations.common_validations import validar_data, validar_campo_obrigatorio
from app.config import Config
from datetime import datetime

bp = Blueprint('feriado', __name__, url_prefix='/feriado')

def _validar_feriado(data, codigo_orgao, descricao, creche=None, recesso=None):
    """RN-01, RN-02, RN-03, RN-04, RN-05, RN-06, RN-07: Validar feriado"""
    errors = []
    
    # RN-01, RN-07: Data DDMMYYYY válida (1994-2099)
    valid, data_obj = validar_data(data)
    if not valid:
        errors.append("Data inválida (formato: DDMMYYYY, 1994-2099)")
    
    # RN-02: Código órgão é parte da chave (obrigatório)
    if not codigo_orgao or not validar_campo_obrigatorio(codigo_orgao):
        errors.append("Código do órgão é obrigatório")
    
    # RN-04: Descrição obrigatória (40 caracteres max)
    if not descricao or not validar_campo_obrigatorio(descricao):
        errors.append("Descrição é obrigatória")
    elif len(descricao) > 40:
        errors.append("Descrição não pode exceder 40 caracteres")
    
    # RN-05: Creche opcional (S/N)
    if creche and creche not in ['S', 'N']:
        errors.append("Creche deve ser 'S', 'N' ou vazio")
    
    # RN-06: recesso_literal literal
    if recesso and recesso not in ['RECESSO', 'RECESSO ESCOLAR']:
        errors.append("Recesso deve ser 'RECESSO', 'RECESSO ESCOLAR' ou vazio")
    
    return len(errors) == 0, "; ".join(errors) if errors else None, data_obj if valid else None

@bp.route('/', methods=['GET'])
def listar():
    """F-008: Consultar feriados do órgão (filtrado por sessão)"""
    page = request.args.get('page', 1, type=int)
    # TODO: Filtrar por código_orgao da sessão quando sessão implementada
    pagination = FERIADO_ORGAO.query.order_by(FERIADO_ORGAO.data.desc()).paginate(page=page, per_page=Config.ITEMS_PER_PAGE)
    return render_template('feriado/lista.html', 
                         feriados=pagination.items, 
                         pagination=pagination, 
                         page=page)

@bp.route('/criar', methods=['GET', 'POST'])
def criar():
    """F-008: Criar novo feriado"""
    if request.method == 'POST':
        data = request.form.get('data', '').strip()
        codigo_orgao = request.form.get('codigo_orgao', '').strip()
        descricao = request.form.get('descricao', '').strip()
        creche = request.form.get('creche', '').strip() or None
        recesso = request.form.get('recesso', '').strip() or None
        
        is_valid, error, data_obj = _validar_feriado(data, codigo_orgao, descricao, creche, recesso)
        if not is_valid:
            flash(f'Erro: {error}', 'danger')
            return render_template('feriado/criar.html')
        
        # RN-01/RN-07: Verificar duplicação (data, órgão)
        feriado_existente = FERIADO_ORGAO.query.filter_by(data=data_obj, codigo_orgao=codigo_orgao).first()
        if feriado_existente:
            flash('Feriado já existe para este órgão nesta data', 'danger')
            return render_template('feriado/criar.html')
        
        try:
            f = FERIADO_ORGAO(
                data=data_obj,
                codigo_orgao=codigo_orgao,
                descricao=descricao,
                creche=creche,
                recesso=recesso
            )
            db.session.add(f)
            db.session.commit()
            
            # Auditoria: Registrar criação
            auditoria = AUDITORIA.registrar(
                tabela='feriado_orgao',
                operacao='CREATE',
                chave_primaria=f"{data_obj.strftime('%d%m%Y')}-{codigo_orgao}",
                valores_novos=f.to_dict(),
                usuario=request.remote_addr
            )
            db.session.add(auditoria)
            db.session.commit()
            
            flash('Feriado criado com sucesso', 'success')
            return redirect(url_for('feriado.listar'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao criar feriado: {str(e)}', 'danger')
    
    return render_template('feriado/criar.html')

@bp.route('/editar/<data>/<codigo_orgao>', methods=['GET', 'POST'])
def editar(data, codigo_orgao):
    """F-008: Editar feriado"""
    valid, data_obj = validar_data(data)
    if not valid:
        flash('Data inválida', 'danger')
        return redirect(url_for('feriado.listar'))
    
    f = FERIADO_ORGAO.query.filter_by(data=data_obj, codigo_orgao=codigo_orgao).first()
    if not f:
        flash('Registro não encontrado', 'danger')
        return redirect(url_for('feriado.listar'))
    
    if request.method == 'POST':
        descricao = request.form.get('descricao', '').strip()
        creche = request.form.get('creche', '').strip() or None
        recesso = request.form.get('recesso', '').strip() or None
        
        is_valid, error, _ = _validar_feriado(data, codigo_orgao, descricao, creche, recesso)
        if not is_valid:
            flash(f'Erro: {error}', 'danger')
            return render_template('feriado/editar.html', feriado=f)
        
        try:
            antes = f.to_dict()
            f.descricao = descricao
            f.creche = creche
            f.recesso = recesso
            db.session.commit()
            
            # Auditoria: Registrar alteração
            auditoria = AUDITORIA.registrar(
                tabela='feriado_orgao',
                operacao='UPDATE',
                chave_primaria=f"{data_obj.strftime('%d%m%Y')}-{codigo_orgao}",
                valores_anteriores=antes,
                valores_novos=f.to_dict(),
                usuario=request.remote_addr
            )
            db.session.add(auditoria)
            db.session.commit()
            
            flash('Feriado atualizado com sucesso', 'success')
            return redirect(url_for('feriado.listar'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar feriado: {str(e)}', 'danger')
    
    return render_template('feriado/editar.html', feriado=f)

@bp.route('/deletar/<data>/<codigo_orgao>', methods=['POST'])
def deletar(data, codigo_orgao):
    """F-008: Deletar feriado"""
    valid, data_obj = validar_data(data)
    if not valid:
        flash('Data inválida', 'danger')
        return redirect(url_for('feriado.listar'))
    
    f = FERIADO_ORGAO.query.filter_by(data=data_obj, codigo_orgao=codigo_orgao).first()
    if not f:
        flash('Registro não encontrado', 'danger')
        return redirect(url_for('feriado.listar'))
    
    try:
        antes = f.to_dict()
        db.session.delete(f)
        db.session.commit()
        
        # Auditoria: Registrar deleção
        auditoria = AUDITORIA.registrar(
            tabela='feriado_orgao',
            operacao='DELETE',
            chave_primaria=f"{data_obj.strftime('%d%m%Y')}-{codigo_orgao}",
            valores_anteriores=antes,
            usuario=request.remote_addr
        )
        db.session.add(auditoria)
        db.session.commit()
        
        flash('Feriado deletado com sucesso', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao deletar feriado: {str(e)}', 'danger')
    
    return redirect(url_for('feriado.listar'))
