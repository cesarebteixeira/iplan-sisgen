"""Routes for Periods (C172T) - F-007
Manter Períodos de Referência
Operações: CON, I (CREATE ONLY - NÃO ALTER, NÃO DELETE)
Validações: RN-01 (ano 4d, 1994-2099), RN-02 (mês 2d, 01-12),
            RN-03 (dia_inicio sempre 1), RN-04 (mes_inicio sempre = mes),
            RN-05 (dia_limite é último dia do mês), RN-06 (mes_limite sempre = mes),
            RN-07 (não permitir duplicação ano, mes)
Escopo: Sistema todo (não por secretaria)
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models.periodo import PERIODO_REFERENCIA
from app.models.auditoria import AUDITORIA
from app.validations.common_validations import validar_ano, validar_mes
from app.config import Config
from calendar import monthrange

bp = Blueprint('periodo', __name__, url_prefix='/periodo')

def _validar_periodo(ano, mes):
    """RN-01, RN-02, RN-07: Validar período de referência"""
    errors = []
    
    # RN-01: Ano 4 dígitos (1994-2099)
    if not ano or not validar_ano(ano):
        errors.append("Ano deve ser numérico entre 1994 e 2099")
    
    # RN-02: Mês 2 dígitos (01-12)
    if not mes or not validar_mes(mes):
        errors.append("Mês deve ser numérico entre 01 e 12")
    
    return len(errors) == 0, "; ".join(errors) if errors else None

@bp.route('/', methods=['GET'])
def listar():
    """F-007: Consultar períodos com paginação"""
    page = request.args.get('page', 1, type=int)
    pagination = PERIODO_REFERENCIA.query.order_by(
        PERIODO_REFERENCIA.ano.desc(), 
        PERIODO_REFERENCIA.mes.desc()
    ).paginate(page=page, per_page=Config.ITEMS_PER_PAGE)
    return render_template('periodo/lista.html', 
                         periodos=pagination.items, 
                         pagination=pagination, 
                         page=page)

@bp.route('/criar', methods=['GET', 'POST'])
def criar():
    """F-007: Criar novo período (CREATE ONLY)"""
    if request.method == 'POST':
        ano = request.form.get('ano', '').strip()
        mes = request.form.get('mes', '').strip()
        
        is_valid, error = _validar_periodo(ano, mes)
        if not is_valid:
            flash(f'Erro: {error}', 'danger')
            return render_template('periodo/criar.html')
        
        try:
            ano_int = int(ano)
            mes_int = int(mes)
        except (ValueError, TypeError):
            flash('Ano e mês devem ser números', 'danger')
            return render_template('periodo/criar.html')
        
        # RN-07: Não permitir duplicação (ano, mes)
        periodo_existente = PERIODO_REFERENCIA.query.filter_by(ano=ano_int, mes=mes_int).first()
        if periodo_existente:
            flash('Período já existe', 'danger')
            return render_template('periodo/criar.html')
        
        try:
            # Calcular last day of month (RN-05)
            _, ultimo_dia = monthrange(ano_int, mes_int)
            
            # RN-03, RN-04, RN-05, RN-06: Campos automáticos
            p = PERIODO_REFERENCIA(
                ano=ano_int,
                mes=mes_int,
                dia_inicio=1,
                mes_inicio=mes_int,
                dia_limite=ultimo_dia,
                mes_limite=mes_int
            )
            db.session.add(p)
            db.session.commit()
            
            # Auditoria: Registrar criação
            auditoria = AUDITORIA.registrar(
                tabela='periodo_referencia',
                operacao='CREATE',
                chave_primaria=f"{ano_int}-{mes_int:02d}",
                valores_novos=p.to_dict(),
                usuario=request.remote_addr
            )
            db.session.add(auditoria)
            db.session.commit()
            
            flash('Período criado com sucesso', 'success')
            return redirect(url_for('periodo.listar'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao criar período: {str(e)}', 'danger')
    
    return render_template('periodo/criar.html')

@bp.route('/api/<int:ano>/<int:mes>', methods=['GET'])
def get_json(ano, mes):
    """API: Retornar período em JSON"""
    from flask import jsonify
    p = PERIODO_REFERENCIA.query.filter_by(ano=ano, mes=mes).first()
    if not p:
        return jsonify({'error': 'Período não encontrado'}), 404
    return jsonify(p.to_dict())
