# -*- coding: utf-8 -*-
"""
PROJETO model - Projects (C205T)
Funcionalidade F-009: Manter Projetos da Secretaria
"""

from datetime import datetime
from app import db

class PROJETO(db.Model):
    """
    Organization projects (PROJETO)
    
    Especificação C205T:
    - Chave Composta: (codigo_projeto, secretaria)
    - Código Projeto: 2 dígitos
    - Secretaria: por secretaria em sessão
    - Descrição: 40 caracteres (obrigatória)
    - Operações: CON, I, A, E (com guarda)
    - Capacidade: 999 por secretaria (0 = blank line)
    - Guarda: Não deletar se vínculos órgão-projeto existem
    - Persistência: Última posição entre reaperturas
    - Paginação: 15 linhas
    """
    __tablename__ = 'projeto'
    
    # COMPOSITE PRIMARY KEY: (codigo_projeto, secretaria)
    codigo_projeto = db.Column(db.Integer, primary_key=True)
    secretaria = db.Column(db.String(255), primary_key=True)
    
    # FIELDS: 40 caracteres máximo, obrigatório
    descricao = db.Column(db.String(40), nullable=False)
    
    # AUDIT FIELDS: auto timestamp
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    data_modificacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships - NOTE: backref='vinculos' is defined in VINCULO_ORGAO_PROJETO.projeto relationship
    
    def __repr__(self):
        return f'<PROJETO {self.codigo_projeto:02d}-{self.secretaria}>'
    
    def to_dict(self):
        """
        Convert to dictionary for audit trail and API responses
        Includes ALL fields for complete audit coverage
        """
        return {
            'codigo_projeto': self.codigo_projeto,
            'secretaria': self.secretaria,
            'descricao': self.descricao,
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None,
            'data_modificacao': self.data_modificacao.isoformat() if self.data_modificacao else None,
        }
