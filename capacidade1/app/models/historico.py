# -*- coding: utf-8 -*-
"""
HISTORICO_PERIODO_ORGAO model - Historical period changes
Funcionalidade F-011: Transferência de Órgãos entre Coordenações
Funcionalidade F-012: Substituição de Órgão Provisório por Definitivo SDI
"""

from datetime import datetime
from app import db

class HISTORICO_PERIODO_ORGAO(db.Model):
    """
    Historical record of period changes and transitions (HISTORICO_PERIODO_ORGAO)
    
    Especificação C225T/C226T:
    - Identificador: ID (auto-increment)
    - Código Órgão: identificador (obrigatório)
    - Período Anterior: YYYY-MM format (referencia TB-007)
    - Período Novo: YYYY-MM format (referencia TB-007)
    - Data Mudança: TIMESTAMP (obrigatória)
    - Tipo Mudança: TRANSFERENCIA, TRANSICAO_SDI, etc
    - Auditoria: Completa com timestamp
    - HISTÓRICO NÃO-DESTRUTIVO: Novos registros adicionados, nunca deletados
    - Reabertura: Permite reverter período fechado (novos registros com auditoria)
    """
    __tablename__ = 'historico_periodo_orgao'
    
    # PRIMARY KEY: auto-increment sequence
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # FIELDS: Código órgão (obrigatório)
    codigo_orgao = db.Column(db.String(255), nullable=False)
    
    # FIELDS: Período anterior (YYYY-MM format, opcional)
    periodo_anterior = db.Column(db.String(10))
    
    # FIELDS: Período novo (YYYY-MM format, obrigatório)
    periodo_novo = db.Column(db.String(10), nullable=False)
    
    # FIELDS: Tipo de mudança (TRANSFERENCIA, TRANSICAO_SDI, etc)
    tipo_mudanca = db.Column(db.String(50), nullable=False)
    
    # AUDIT FIELDS: timestamp da mudança (obrigatório)
    data_mudanca = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # AUDIT FIELDS: criação do registro de histórico
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<HISTORICO_PERIODO_ORGAO {self.id} - {self.tipo_mudanca}>'
    
    def to_dict(self):
        """
        Convert to dictionary for audit trail and API responses
        Includes ALL fields for complete audit coverage
        """
        return {
            'id': self.id,
            'codigo_orgao': self.codigo_orgao,
            'periodo_anterior': self.periodo_anterior,
            'periodo_novo': self.periodo_novo,
            'tipo_mudanca': self.tipo_mudanca,
            'data_mudanca': self.data_mudanca.isoformat() if self.data_mudanca else None,
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None,
        }
