# -*- coding: utf-8 -*-
"""
BAIRRO model - Neighborhoods (C023T)
Funcionalidade F-001: Manter Bairros
"""

from datetime import datetime
from app import db

class BAIRRO(db.Model):
    """
    Neighborhood classification (BAIRRO)
    
    Especificação C023T:
    - Código: 3 dígitos (auto-increment, inicia em 1)
    - Descrição: 25 caracteres (obrigatória)
    - Operações: CON, I, E (sem ALTER)
    - Paginação: 15 linhas
    """
    __tablename__ = 'bairro'
    
    # PRIMARY KEY: 3 dígitos, auto-increment a partir de 1
    # IMPORTANTE: Para SQLite, usar INTEGER PRIMARY KEY sem NOT NULL para autoincrement automático
    codigo_bairro = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # FIELDS: 25 caracteres máximo, obrigatório
    descricao = db.Column(db.String(25), nullable=False)
    
    # AUDIT FIELDS: auto timestamp
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    data_modificacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<BAIRRO {self.codigo_bairro}>'
    
    def to_dict(self):
        """
        Convert to dictionary for audit trail and API responses
        Includes ALL fields for complete audit coverage
        """
        return {
            'codigo_bairro': self.codigo_bairro,
            'descricao': self.descricao,
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None,
            'data_modificacao': self.data_modificacao.isoformat() if self.data_modificacao else None,
        }
