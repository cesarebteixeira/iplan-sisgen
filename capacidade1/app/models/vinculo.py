# -*- coding: utf-8 -*-
"""
VINCULO_ORGAO_PROJETO model - Institutional links (C207T)
Funcionalidade F-010: Vínculos Órgão-Projeto
"""

from datetime import datetime
from app import db

class VINCULO_ORGAO_PROJETO(db.Model):
    """
    Links between organizational units and projects (VINCULO_ORGAO_PROJETO)
    
    Especificação C207T:
    - Chave Composta: (codigo_orgao, codigo_projeto, secretaria)
    - Código Órgão: identificador (obrigatório)
    - Código Projeto: 2 dígitos (FOREIGN KEY para PROJETO, obrigatório)
    - Secretaria: FOREIGN KEY para PROJETO (obrigatória)
    - Coordenadoria: reference field (opcional)
    - Operações: CON, I, E (NO ALTER)
    - Validações: Órgão deve existir, projeto deve existir
    - Persistência: Última posição
    - Paginação: 13 linhas
    - Nota: Validação básica de existência; restrição "órgão completo" removida
    """
    __tablename__ = 'vinculo_orgao_projeto'
    
    # COMPOSITE PRIMARY KEY: (codigo_orgao, codigo_projeto, secretaria)
    codigo_orgao = db.Column(db.String(255), primary_key=True)
    codigo_projeto = db.Column(db.Integer, primary_key=True)
    secretaria = db.Column(db.String(255), primary_key=True)
    
    # OPTIONAL: Reference field for coordination
    coordenadoria = db.Column(db.String(255))
    
    # AUDIT FIELDS: creation only (no update for links)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    data_modificacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Foreign Key Constraint: (codigo_projeto, secretaria) → PROJETO
    __table_args__ = (
        db.ForeignKeyConstraint(
            ['codigo_projeto', 'secretaria'],
            ['projeto.codigo_projeto', 'projeto.secretaria']
        ),
    )
    
    # Relationships
    projeto = db.relationship('PROJETO', backref='vinculos', foreign_keys=[codigo_projeto, secretaria])
    
    def __repr__(self):
        return f'<VINCULO_ORGAO_PROJETO {self.codigo_orgao}-{self.codigo_projeto:02d}>'
    
    def to_dict(self):
        """
        Convert to dictionary for audit trail and API responses
        Includes ALL fields for complete audit coverage
        """
        return {
            'codigo_orgao': self.codigo_orgao,
            'codigo_projeto': self.codigo_projeto,
            'secretaria': self.secretaria,
            'coordenadoria': self.coordenadoria,
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None,
            'data_modificacao': self.data_modificacao.isoformat() if self.data_modificacao else None,
        }
