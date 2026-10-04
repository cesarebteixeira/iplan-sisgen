# -*- coding: utf-8 -*-
"""
UNIDADE_ORCAMENTARIA model - Budgetary units (C025T)
Funcionalidade F-002: Manter Unidades Orçamentárias
"""

from datetime import datetime
from app import db

class UNIDADE_ORCAMENTARIA(db.Model):
    """
    Budgetary organizational units (UNIDADE_ORCAMENTARIA)
    
    Especificação C025T:
    - Código: 8 dígitos (PRIMARY KEY)
    - Descrição: 40 caracteres (obrigatória)
    - Operações: CON, I, A, E
    - Capacidade: 1.500.000 unidades
    - Guarda: Não deletar se grupos ou contratos existem
    - Paginação: 15 linhas
    """
    __tablename__ = 'unidade_orcamentaria'
    
    # PRIMARY KEY: 8 dígitos
    codigo_unidade = db.Column(db.String(8), primary_key=True)
    
    # FIELDS: 40 caracteres máximo, obrigatório
    descricao = db.Column(db.String(40), nullable=False)
    
    # AUDIT FIELDS: auto timestamp
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    data_modificacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    grupos = db.relationship('GRUPO', backref='unidade', lazy=True)
    
    def __repr__(self):
        return f'<UNIDADE_ORCAMENTARIA {self.codigo_unidade}>'
    
    def to_dict(self):
        """
        Convert to dictionary for audit trail and API responses
        Includes ALL fields for complete audit coverage
        """
        return {
            'codigo_unidade': self.codigo_unidade,
            'descricao': self.descricao,
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None,
            'data_modificacao': self.data_modificacao.isoformat() if self.data_modificacao else None,
        }
