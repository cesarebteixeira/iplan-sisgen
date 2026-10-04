"""Routes for Institutional Links (C207T) - F-010
Vínculos Órgão-Projeto
Operações: CON, I, E (NO ALTER - NÃO implementar editar)
Validações: RN-01 (código_orgao parte da chave), RN-02 (código_projeto 2d obrigatório, deve existir),
            RN-03 (secretaria obrigatória, deve existir), RN-04 (coordenadoria opcional),
            RN-05 (órgão deve existir completo - 6 campos preenchidos)
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app import db
from app.models.vinculo import VINCULO_ORGAO_PROJETO
from app.models.projeto import PROJETO
from app.models.auditoria import AUDITORIA
from app.validations.common_validations import validar_campo_obrigatorio, validar_numerico
from app.config import Config

bp = Blueprint('vinculo', __name__, url_prefix='/vinculo')

def _validar_vinculo(codigo_orgao, codigo_projeto):
    """RN-01, RN-02: Validar vínculo órgão-projeto"""
    errors = []
    
    # RN-01: Código órgão é parte da chave (obrigatório)
    if not codigo_orgao or not validar_campo_obrigatorio(codigo_orgao):
        errors.append("Código do órgão é obrigatório")
    
    # RN-02: Código projeto 2 dígitos obrigatório e deve existir
    if not codigo_projeto or not validar_numerico(codigo_projeto):
        errors.append("Código do projeto deve conter apenas números")
    elif len(codigo_projeto) != 2:
        errors.append("Código do projeto deve ter exatamente 2 dígitos")
    elif not PROJETO.query.filter_by(codigo_projeto=int(codigo_projeto)).first():
        errors.append("Projeto não encontrado")
    
    return len(errors) == 0, "; ".join(errors) if errors else None

def _verificar_orgao_completo(codigo_orgao):
    """RN-05: Verificar se órgão existe com 6 campos preenchidos (completo)"""
    # TODO: Integrar com modelo ORGAO quando disponível
    # Por enquanto, retorna True (validação básica de existência)
    return True

@bp.route('/', methods=['GET'])
def listar():
    """F-010: Consultar vínculos órgão-projeto com paginação"""
    page = request.args.get('page', 1, type=int)
    pagination = VINCULO_ORGAO_PROJETO.query.order_by(
        VINCULO_ORGAO_PROJETO.codigo_orgao, 
        VINCULO_ORGAO_PROJETO.codigo_projeto
    ).paginate(page=page, per_page=Config.ITEMS_PER_PAGE)
    return render_template('vinculo/lista.html', 
                         vinculos=pagination.items, 
                         pagination=pagination, 
                         page=page)

@bp.route('/criar', methods=['GET', 'POST'])
def criar():
    """F-010: Criar novo vínculo órgão-projeto (NO ALTER, apenas I/E)"""
    if request.method == 'POST':
        codigo_orgao = request.form.get('codigo_orgao', '').strip()
        codigo_projeto = request.form.get('codigo_projeto', '').strip()
        
        is_valid, error = _validar_vinculo(codigo_orgao, codigo_projeto)
        if not is_valid:
            flash(f'Erro: {error}', 'danger')
            return render_template('vinculo/criar.html', projetos=PROJETO.query.all())
        
        # RN-05: Validar que órgão existe e é completo
        if not _verificar_orgao_completo(codigo_orgao):
            flash('Órgão não encontrado ou incompleto', 'danger')
            return render_template('vinculo/criar.html', projetos=PROJETO.query.all())
        
        # Verificar duplicação
        vinculo_existente = VINCULO_ORGAO_PROJETO.query.filter_by(
            codigo_orgao=codigo_orgao,
            codigo_projeto=int(codigo_projeto)
        ).first()
        if vinculo_existente:
            flash('Vínculo já existe entre este órgão e projeto', 'danger')
            return render_template('vinculo/criar.html', projetos=PROJETO.query.all())
        
        try:
            vinculo = VINCULO_ORGAO_PROJETO(
                codigo_orgao=codigo_orgao,
                codigo_projeto=int(codigo_projeto)
            )
            db.session.add(vinculo)
            db.session.commit()
            
            # Auditoria: Registrar criação
            auditoria = AUDITORIA.registrar(
                tabela='vinculo_orgao_projeto',
                operacao='CREATE',
                chave_primaria=f"{codigo_orgao}-{codigo_projeto}",
                valores_novos=vinculo.to_dict(),
                usuario=request.remote_addr
            )
            db.session.add(auditoria)
            db.session.commit()
            
            flash('Vínculo criado com sucesso', 'success')
            return redirect(url_for('vinculo.listar'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao criar vínculo: {str(e)}', 'danger')
    
    projetos = PROJETO.query.all()
    return render_template('vinculo/criar.html', projetos=projetos)

@bp.route('/deletar/<codigo_orgao>/<codigo_projeto>', methods=['POST'])
def deletar(codigo_orgao, codigo_projeto):
    """F-010: Deletar vínculo órgão-projeto (NO ALTER - apenas I/E)"""
    try:
        codigo_projeto_int = int(codigo_projeto)
    except (ValueError, TypeError):
        flash('Código de projeto inválido', 'danger')
        return redirect(url_for('vinculo.listar'))
    
    vinculo = VINCULO_ORGAO_PROJETO.query.filter_by(
        codigo_orgao=codigo_orgao,
        codigo_projeto=codigo_projeto_int
    ).first()
    if not vinculo:
        flash('Registro não encontrado', 'danger')
        return redirect(url_for('vinculo.listar'))
    
    try:
        antes = vinculo.to_dict()
        db.session.delete(vinculo)
        db.session.commit()
        
        # Auditoria: Registrar deleção
        auditoria = AUDITORIA.registrar(
            tabela='vinculo_orgao_projeto',
            operacao='DELETE',
            chave_primaria=f"{codigo_orgao}-{codigo_projeto_int}",
            valores_anteriores=antes,
            usuario=request.remote_addr
        )
        db.session.add(auditoria)
        db.session.commit()
        
        flash('Vínculo deletado com sucesso', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao deletar vínculo: {str(e)}', 'danger')
    
    return redirect(url_for('vinculo.listar'))

@bp.route('/api/<codigo_orgao>/<codigo_projeto>', methods=['GET'])
def get_json(codigo_orgao, codigo_projeto):
    """API: Retornar vínculo em JSON"""
    try:
        codigo_projeto_int = int(codigo_projeto)
    except (ValueError, TypeError):
        return jsonify({'error': 'Código de projeto inválido'}), 400
    
    vinculo = VINCULO_ORGAO_PROJETO.query.filter_by(
        codigo_orgao=codigo_orgao,
        codigo_projeto=codigo_projeto_int
    ).first()
    if not vinculo:
        return jsonify({'error': 'Vínculo não encontrado'}), 404
    return jsonify(vinculo.to_dict())
