"""Routes for Accounts (C147T) - F-005
Classificar Contas
Operações: CON, I, A (apenas campo creche, NÃO fonte), E
Validações: RN-01 (conta é chave), RN-02 (código_orgao é parte da chave),
            RN-03 (código_fonte 7d obrigatório, deve existir),
            RN-04 (creche S/N obrigatório),
            RN-05/RN-06 (BLOQUEADO alterar código_fonte)
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models.conta import CONTA_CLASSIFICADA
from app.models.fonte import FONTE_RECURSOS
from app.models.auditoria import AUDITORIA
from app.validations.common_validations import validar_campo_obrigatorio, validar_numerico
from app.config import Config

bp = Blueprint('conta', __name__, url_prefix='/conta')

def _validar_conta(conta, codigo_orgao, codigo_fonte, creche):
    """RN-01, RN-02, RN-03, RN-04: Validar conta classificada"""
    errors = []
    
    # RN-01: Conta é chave primária
    if not conta or not validar_campo_obrigatorio(conta):
        errors.append("Conta é obrigatória")
    
    # RN-02: Código órgão é parte da chave
    if not codigo_orgao or not validar_campo_obrigatorio(codigo_orgao):
        errors.append("Código do órgão é obrigatório")
    
    # RN-03: Código fonte 7 dígitos obrigatório e deve existir
    if not codigo_fonte or not validar_numerico(codigo_fonte):
        errors.append("Código da fonte deve conter apenas números")
    elif len(codigo_fonte) != 7:
        errors.append("Código da fonte deve ter exatamente 7 dígitos")
    elif not FONTE_RECURSOS.query.filter_by(codigo_fonte=codigo_fonte).first():
        errors.append("Fonte não encontrada")
    
    # RN-04: Creche S/N obrigatório
    if creche not in ['S', 'N']:
        errors.append("Creche deve ser 'S' ou 'N'")
    
    return len(errors) == 0, "; ".join(errors) if errors else None

@bp.route('/', methods=['GET'])
def listar():
    """F-005: Consultar contas classificadas (filtrado por órgão em sessão)"""
    page = request.args.get('page', 1, type=int)
    # TODO: Filtrar por código_orgao da sessão quando sessão implementada
    pagination = CONTA_CLASSIFICADA.query.order_by(CONTA_CLASSIFICADA.conta).paginate(page=page, per_page=Config.ITEMS_PER_PAGE)
    return render_template('conta/lista.html', 
                         contas=pagination.items, 
                         pagination=pagination, 
                         page=page)

@bp.route('/criar', methods=['GET', 'POST'])
def criar():
    """F-005: Criar nova classificação de conta"""
    if request.method == 'POST':
        conta = request.form.get('conta', '').strip()
        codigo_orgao = request.form.get('codigo_orgao', '').strip()
        codigo_fonte = request.form.get('codigo_fonte', '').strip()
        creche = request.form.get('creche', '').strip()
        
        is_valid, error = _validar_conta(conta, codigo_orgao, codigo_fonte, creche)
        if not is_valid:
            flash(f'Erro: {error}', 'danger')
            return render_template('conta/criar.html', fontes=FONTE_RECURSOS.query.all())
        
        # RN-03: Verificar que fonte existe para este órgão
        fonte = FONTE_RECURSOS.query.filter_by(codigo_fonte=codigo_fonte, codigo_orgao=codigo_orgao).first()
        if not fonte:
            flash('Fonte não encontrada para este órgão', 'danger')
            return render_template('conta/criar.html', fontes=FONTE_RECURSOS.query.all())
        
        # RN-03: Não permitir duplicação com mesma fonte
        conta_existente = CONTA_CLASSIFICADA.query.filter_by(
            conta=conta,
            codigo_orgao=codigo_orgao,
            codigo_fonte=codigo_fonte
        ).first()
        if conta_existente:
            flash('Conta já está classificada com esta fonte neste órgão', 'danger')
            return render_template('conta/criar.html', fontes=FONTE_RECURSOS.query.all())
        
        try:
            c = CONTA_CLASSIFICADA(
                conta=conta,
                codigo_orgao=codigo_orgao,
                codigo_fonte=codigo_fonte,
                creche=creche
            )
            db.session.add(c)
            db.session.commit()
            
            # Auditoria: Registrar criação
            auditoria = AUDITORIA.registrar(
                tabela='conta_classificada',
                operacao='CREATE',
                chave_primaria=f"{conta}-{codigo_orgao}",
                valores_novos=c.to_dict(),
                usuario=request.remote_addr
            )
            db.session.add(auditoria)
            db.session.commit()
            
            flash('Conta criada com sucesso', 'success')
            return redirect(url_for('conta.listar'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao criar conta: {str(e)}', 'danger')
    
    return render_template('conta/criar.html', fontes=FONTE_RECURSOS.query.all())

@bp.route('/editar/<conta>/<codigo_orgao>', methods=['GET', 'POST'])
def editar(conta, codigo_orgao):
    """F-005: Editar conta (RN-05/RN-06: BLOQUEADO alterar código_fonte, apenas creche)"""
    c = CONTA_CLASSIFICADA.query.filter_by(conta=conta, codigo_orgao=codigo_orgao).first()
    if not c:
        flash('Registro não encontrado', 'danger')
        return redirect(url_for('conta.listar'))
    
    if request.method == 'POST':
        creche = request.form.get('creche', '').strip()
        
        # RN-05: Validar que código_fonte não foi alterado
        codigo_fonte_form = request.form.get('codigo_fonte', '').strip()
        if codigo_fonte_form != c.codigo_fonte:
            flash('Alteração de código da fonte é bloqueada. Apenas o campo creche pode ser alterado.', 'danger')
            return render_template('conta/editar.html', conta=c)
        
        # RN-04: Creche S/N obrigatório
        if creche not in ['S', 'N']:
            flash('Creche deve ser "S" ou "N"', 'danger')
            return render_template('conta/editar.html', conta=c)
        
        try:
            antes = c.to_dict()
            c.creche = creche
            db.session.commit()
            
            # Auditoria: Registrar alteração com restrição aplicada
            auditoria = AUDITORIA.registrar(
                tabela='conta_classificada',
                operacao='UPDATE',
                chave_primaria=f"{conta}-{codigo_orgao}",
                valores_anteriores=antes,
                valores_novos=c.to_dict(),
                usuario=request.remote_addr,
                observacao='Apenas campo creche foi alterado (RN-05: código_fonte bloqueado)'
            )
            db.session.add(auditoria)
            db.session.commit()
            
            flash('Conta atualizada com sucesso', 'success')
            return redirect(url_for('conta.listar'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar conta: {str(e)}', 'danger')
    
    return render_template('conta/editar.html', conta=c, codigo_fonte_readonly=True)

@bp.route('/deletar/<conta>/<codigo_orgao>', methods=['POST'])
def deletar(conta, codigo_orgao):
    """F-005: Deletar classificação de conta"""
    c = CONTA_CLASSIFICADA.query.filter_by(conta=conta, codigo_orgao=codigo_orgao).first()
    if not c:
        flash('Registro não encontrado', 'danger')
        return redirect(url_for('conta.listar'))
    
    try:
        antes = c.to_dict()
        db.session.delete(c)
        db.session.commit()
        
        # Auditoria: Registrar deleção
        auditoria = AUDITORIA.registrar(
            tabela='conta_classificada',
            operacao='DELETE',
            chave_primaria=f"{conta}-{codigo_orgao}",
            valores_anteriores=antes,
            usuario=request.remote_addr
        )
        db.session.add(auditoria)
        db.session.commit()
        
        flash('Conta deletada com sucesso', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao deletar conta: {str(e)}', 'danger')
    
    return redirect(url_for('conta.listar'))
