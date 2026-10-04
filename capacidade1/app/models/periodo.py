# -*- coding: utf-8 -*-
"""
PERIODO_REFERENCIA model - Reference periods (C172T)
Funcionalidade F-007: Manter Períodos de Referência
"""

from datetime import datetime
from app import db

class PERIODO_REFERENCIA(db.Model):
    """
    Fiscal reference periods (PERIODO_REFERENCIA)
    
    Especificação C172T:
    - Chave Composta: (ano, mes)
    - Ano: 4 dígitos (1994-2099)
    - Mês: 2 dígitos (01-12)
    - Dia Início: 2 dígitos (always 1)
    - Mês Início: 2 dígitos (always = mes)
    - Dia Limite: 2 dígitos (last day of month)
    - Mês Limite: 2 dígitos (always = mes)
    - Operações: CON, I (criar apenas, NO ALTER, NO DELETE)
    - Escopo: Sistema todo
    - Paginação: 13 linhas
    """
    __tablename__ = 'periodo_referencia'
    
    # COMPOSITE PRIMARY KEY: (ano, mes)
    ano = db.Column(db.Integer, primary_key=True)
    mes = db.Column(db.Integer, primary_key=True)
    
    # TECHNICAL FIELDS: computed/static
    dia_inicio = db.Column(db.Integer, default=1)  # always 1
    mes_inicio = db.Column(db.Integer)  # always = mes
    dia_limite = db.Column(db.Integer)  # last day of month (28/29/30/31)
    mes_limite = db.Column(db.Integer)  # always = mes
    
    # AUDIT FIELDS: creation only (no update for periods)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<PERIODO_REFERENCIA {self.ano}-{self.mes:02d}>'
    
    def to_dict(self):
        """
        Convert to dictionary for audit trail and API responses
        Includes ALL fields for complete audit coverage
        """
        return {
            'ano': self.ano,
            'mes': self.mes,
            'dia_inicio': self.dia_inicio,
            'mes_inicio': self.mes_inicio,
            'dia_limite': self.dia_limite,
            'mes_limite': self.mes_limite,
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None,
        }
