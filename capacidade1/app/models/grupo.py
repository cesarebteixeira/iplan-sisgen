# -*- coding: utf-8 -*-
"""
GRUPO model - Organizational groups (C126T)
Funcionalidade F-003: Manter Grupos/Coordenações
"""

from datetime import datetime
from app import db

class GRUPO(db.Model):
    """
    Organizational groups within units (GRUPO)
    
    Especificação C126T:
    - Chave Composta: (codigo_grupo, tipo_orgao)
    - Código: 2 dígitos
    - Descrição: 40 caracteres (obrigatória)
    - Unidade: 8 dígitos (FOREIGN KEY para UNIDADE_ORCAMENTARIA)
    - Operações: CON (filtrado por tipo órgão), I, A (com propagação), E (com guarda)
    - Capacidade: 1.000 grupos
    - PROPAGAÇÃO: Alteração de unidade propaga para TODOS os órgãos do grupo
    - Guarda: Não deletar se órgãos existem
    - Paginação: 15 linhas
    """
    __tablename__ = 'grupo'
    
    # COMPOSITE PRIMARY KEY: (codigo_grupo, tipo_orgao)
    codigo_grupo = db.Column(db.Integer, primary_key=True)
    tipo_orgao = db.Column(db.String(255), primary_key=True)
    
    # FOREIGN KEY: 8 dígitos referenciando UNIDADE_ORCAMENTARIA
    codigo_unidade = db.Column(db.String(8), db.ForeignKey('unidade_orcamentaria.codigo_unidade'), nullable=False)
    
    # FIELDS: 40 caracteres máximo, obrigatório
    descricao = db.Column(db.String(40), nullable=False)
    
    # AUDIT FIELDS: auto timestamp
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    data_modificacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<GRUPO {self.codigo_grupo:02d}-{self.tipo_orgao}>'
    
    def to_dict(self):
        """
        Convert to dictionary for audit trail and API responses
        Includes ALL fields for complete audit coverage
        """
        return {
            'codigo_grupo': self.codigo_grupo,
            'tipo_orgao': self.tipo_orgao,
            'codigo_unidade': self.codigo_unidade,
            'descricao': self.descricao,
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None,
            'data_modificacao': self.data_modificacao.isoformat() if self.data_modificacao else None,
        }
