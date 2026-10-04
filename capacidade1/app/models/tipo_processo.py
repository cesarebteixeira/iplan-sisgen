# -*- coding: utf-8 -*-
"""
TIPO_PROCESSO model - Process types (C162T)
Funcionalidade F-006: Manter Tipos de Processo
"""

from datetime import datetime
from app import db

class TIPO_PROCESSO(db.Model):
    """
    Types of administrative processes (TIPO_PROCESSO)
    
    Especificação C162T:
    - Chave Composta: (codigo_tipo, tipo_orgao)
    - Código Tipo: 2 dígitos
    - Tipo Órgão: por tipo órgão em sessão
    - Descrição: 40 caracteres (obrigatória)
    - Operações: CON (filtrado por tipo órgão), I, A
    - Capacidade: 1.000 tipos
    - Persistência: Última posição entre reaperturas
    - Paginação: 15 linhas
    """
    __tablename__ = 'tipo_processo'
    
    # COMPOSITE PRIMARY KEY: (codigo_tipo, tipo_orgao)
    codigo_tipo = db.Column(db.Integer, primary_key=True)
    tipo_orgao = db.Column(db.String(255), primary_key=True)
    
    # FIELDS: 40 caracteres máximo, obrigatório
    descricao = db.Column(db.String(40), nullable=False)
    
    # AUDIT FIELDS: auto timestamp
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    data_modificacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<TIPO_PROCESSO {self.codigo_tipo:02d}-{self.tipo_orgao}>'
    
    def to_dict(self):
        """
        Convert to dictionary for audit trail and API responses
        Includes ALL fields for complete audit coverage
        """
        return {
            'codigo_tipo': self.codigo_tipo,
            'tipo_orgao': self.tipo_orgao,
            'descricao': self.descricao,
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None,
            'data_modificacao': self.data_modificacao.isoformat() if self.data_modificacao else None,
        }
