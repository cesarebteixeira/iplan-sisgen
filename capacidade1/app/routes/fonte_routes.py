"""Routes for Sources (C144T) - F-004
Manter Fontes de Recursos
Operações: CON, I, E, U (CRUD completo)
Validações: RN-01 (7d código), RN-02 (desc 30c), RN-03 (código órgão parte da chave),
            RN-04 (ind_FNDE opcional S/N)
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app import db
from app.models.fonte import FONTE_RECURSOS
from app.models.auditoria import AUDITORIA
from app.config import Config

bp = Blueprint('fonte', __name__, url_prefix='/fonte')

def _validar_fonte(codigo_fonte, codigo_orgao, descricao, ind_fnde=''):
    """Validar dados da fonte"""
    errors = []
    
    # RN-01: Código deve ter 7 dígitos
    if not codigo_fonte or not codigo_fonte.isdigit() or len(codigo_fonte) != 7:
        errors.append("Código fonte deve ter exatamente 7 dígitos")
    
    # RN-03: Código órgão obrigatório
    if not codigo_orgao or len(codigo_orgao.strip()) == 0:
        errors.append("Código órgão é obrigatório")
    
    # RN-02: Descrição obrigatória (30 caracteres max)
    if not descricao or len(descricao.strip()) == 0:
        errors.append("Descrição é obrigatória")
    elif len(descricao) > 30:
        errors.append("Descrição não pode exceder 30 caracteres")
    
    # RN-04: FNDE deve ser S, N ou vazio
    if ind_fnde and ind_fnde.upper() not in ['S', 'N', '']:
        errors.append("Indicador FNDE deve ser 'S', 'N' ou vazio")
    
    return len(errors) == 0, "; ".join(errors) if errors else None

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

@bp.route('/criar', methods=['GET', 'POST'])
def criar():
    """F-004: Criar nova fonte de recursos"""
    if request.method == 'POST':
        codigo_fonte = request.form.get('codigo_fonte', '').strip()
        codigo_orgao = request.form.get('codigo_orgao', '').strip()
        descricao = request.form.get('descricao', '').strip()
        ind_fnde = request.form.get('ind_fnde', '').strip().upper() if request.form.get('ind_fnde') else ''
        
        is_valid, error = _validar_fonte(codigo_fonte, codigo_orgao, descricao, ind_fnde)
        if not is_valid:
            flash(f'Erro: {error}', 'danger')
            return render_template('fonte/criar.html')
        
        # Verificar duplicação
        if FONTE_RECURSOS.query.filter_by(codigo_fonte=codigo_fonte, codigo_orgao=codigo_orgao).first():
            flash('Fonte com este código e órgão já existe', 'danger')
            return render_template('fonte/criar.html')
        
        try:
            fonte = FONTE_RECURSOS(
                codigo_fonte=codigo_fonte,
                codigo_orgao=codigo_orgao,
                descricao=descricao,
                ind_fnde=ind_fnde if ind_fnde else None
            )
            db.session.add(fonte)
            db.session.commit()
            
            # Auditoria: Registrar criação
            auditoria = AUDITORIA.registrar(
                tabela='fonte_recursos',
                operacao='CREATE',
                chave_primaria=f'{codigo_fonte}-{codigo_orgao}',
                valores_novos=fonte.to_dict(),
                usuario=request.remote_addr
            )
            db.session.add(auditoria)
            db.session.commit()
            
            flash('Fonte criada com sucesso', 'success')
            return redirect(url_for('fonte.listar'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao criar fonte: {str(e)}', 'danger')
    
    return render_template('fonte/criar.html')

@bp.route('/editar/<codigo_fonte>/<codigo_orgao>', methods=['GET', 'POST'])
def editar(codigo_fonte, codigo_orgao):
    """F-004: Editar fonte de recursos"""
    fonte = FONTE_RECURSOS.query.filter_by(codigo_fonte=codigo_fonte, codigo_orgao=codigo_orgao).first()
    if not fonte:
        flash('Fonte não encontrada', 'danger')
        return redirect(url_for('fonte.listar'))
    
    if request.method == 'POST':
        descricao = request.form.get('descricao', '').strip()
        ind_fnde = request.form.get('ind_fnde', '').strip().upper() if request.form.get('ind_fnde') else ''
        
        # Validar apenas descricao e ind_fnde (código e órgão não mudam)
        if not descricao or len(descricao.strip()) == 0:
            flash('Erro: Descrição é obrigatória', 'danger')
            return render_template('fonte/editar.html', fonte=fonte)
        elif len(descricao) > 30:
            flash('Erro: Descrição não pode exceder 30 caracteres', 'danger')
            return render_template('fonte/editar.html', fonte=fonte)
        
        if ind_fnde and ind_fnde.upper() not in ['S', 'N', '']:
            flash('Erro: Indicador FNDE deve ser S, N ou vazio', 'danger')
            return render_template('fonte/editar.html', fonte=fonte)
        
        try:
            # Guardar valores anteriores para auditoria
            valores_anteriores = fonte.to_dict()
            
            fonte.descricao = descricao
            fonte.ind_fnde = ind_fnde if ind_fnde else None
            db.session.commit()
            
            # Auditoria: Registrar edição
            auditoria = AUDITORIA.registrar(
                tabela='fonte_recursos',
                operacao='UPDATE',
                chave_primaria=f'{codigo_fonte}-{codigo_orgao}',
                valores_anteriores=valores_anteriores,
                valores_novos=fonte.to_dict(),
                usuario=request.remote_addr
            )
            db.session.add(auditoria)
            db.session.commit()
            
            flash('Fonte atualizada com sucesso', 'success')
            return redirect(url_for('fonte.listar'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao editar fonte: {str(e)}', 'danger')
    
    return render_template('fonte/editar.html', fonte=fonte)

@bp.route('/deletar/<codigo_fonte>/<codigo_orgao>', methods=['POST'])
def deletar(codigo_fonte, codigo_orgao):
    """F-004: Deletar fonte de recursos"""
    fonte = FONTE_RECURSOS.query.filter_by(codigo_fonte=codigo_fonte, codigo_orgao=codigo_orgao).first()
    if not fonte:
        flash('Fonte não encontrada', 'danger')
        return redirect(url_for('fonte.listar'))
    
    try:
        valores_anteriores = fonte.to_dict()
        db.session.delete(fonte)
        db.session.commit()
        
        # Auditoria: Registrar deleção
        auditoria = AUDITORIA.registrar(
            tabela='fonte_recursos',
            operacao='DELETE',
            chave_primaria=f'{codigo_fonte}-{codigo_orgao}',
            valores_anteriores=valores_anteriores,
            usuario=request.remote_addr
        )
        db.session.add(auditoria)
        db.session.commit()
        
        flash('Fonte deletada com sucesso', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao deletar fonte: {str(e)}', 'danger')
    
    return redirect(url_for('fonte.listar'))

@bp.route('/api/<codigo_fonte>/<codigo_orgao>', methods=['GET'])
def get_json(codigo_fonte, codigo_orgao):
    """F-004: API - Retornar fonte em JSON"""
    fonte = FONTE_RECURSOS.query.filter_by(codigo_fonte=codigo_fonte, codigo_orgao=codigo_orgao).first()
    if not fonte:
        return jsonify({'error': 'Fonte não encontrada'}), 404
    return jsonify(fonte.to_dict())
