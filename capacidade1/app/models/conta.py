# -*- coding: utf-8 -*-
"""
CONTA_CLASSIFICADA model - Classified accounts (C147T)
Funcionalidade F-005: Classificar Contas
"""

from datetime import datetime
from app import db

class CONTA_CLASSIFICADA(db.Model):
    """
    Classified financial accounts (CONTA_CLASSIFICADA)
    
    Especificação C147T:
    - Chave Composta: (conta, codigo_orgao)
    - Conta: identificador (obrigatório)
    - Código Órgão: por órgão em sessão (obrigatório)
    - Código Fonte: 7 dígitos (FOREIGN KEY para FONTE_RECURSOS, obrigatório)
    - Creche: S ou N (obrigatório)
    - Operações: CON, I, A (apenas campo creche, NÃO fonte), E
    - RESTRIÇÃO: Mudança de fonte BLOQUEADA por RN-05
    - Paginação: 15 linhas
    """
    __tablename__ = 'conta_classificada'
    
    # COMPOSITE PRIMARY KEY: (conta, codigo_orgao)
    conta = db.Column(db.String(255), primary_key=True)
    codigo_orgao = db.Column(db.String(255), primary_key=True)
    
    # FOREIGN KEY: 7 dígitos referenciando FONTE_RECURSOS (obrigatório)
    codigo_fonte = db.Column(db.String(7), nullable=False)
    
    # FIELD: S ou N (obrigatório)
    creche = db.Column(db.String(1), nullable=False)
    
    # AUDIT FIELDS: auto timestamp
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    data_modificacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Foreign key constraint: (codigo_fonte, codigo_orgao) → FONTE_RECURSOS
    __table_args__ = (
        db.ForeignKeyConstraint(
            ['codigo_fonte', 'codigo_orgao'],
            ['fonte_recursos.codigo_fonte', 'fonte_recursos.codigo_orgao']
        ),
    )
    
    # Relationships
    fonte = db.relationship('FONTE_RECURSOS', backref='contas', lazy=True)
    
    def __repr__(self):
        return f'<CONTA_CLASSIFICADA {self.conta}-{self.codigo_orgao}>'
    
    def to_dict(self):
        """
        Convert to dictionary for audit trail and API responses
        Includes ALL fields for complete audit coverage
        """
        return {
            'conta': self.conta,
            'codigo_orgao': self.codigo_orgao,
            'codigo_fonte': self.codigo_fonte,
            'creche': self.creche,
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None,
            'data_modificacao': self.data_modificacao.isoformat() if self.data_modificacao else None,
        }
