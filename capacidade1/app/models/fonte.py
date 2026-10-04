# -*- coding: utf-8 -*-
"""
FONTE_RECURSOS model - Funding sources (C144T)
Funcionalidade F-004: Manter Fontes de Recursos
"""

from datetime import datetime
from app import db

class FONTE_RECURSOS(db.Model):
    """
    Funding sources for accounts (FONTE_RECURSOS)
    
    Especificação C144T:
    - Chave Composta: (codigo_fonte, codigo_orgao)
    - Código Fonte: 7 dígitos
    - Código Órgão: por órgão em sessão
    - Descrição: 30 caracteres (obrigatória)
    - Indicador FNDE: S ou N (opcional)
    - Operações: CON apenas (READ ONLY)
    - Capacidade: 1.000 fontes por órgão
    - Paginação: 15 linhas
    - RESTRIÇÃO: Esta jornada abre apenas CON; não implementar I/A
    """
    __tablename__ = 'fonte_recursos'
    
    # COMPOSITE PRIMARY KEY: (codigo_fonte, codigo_orgao)
    codigo_fonte = db.Column(db.String(7), primary_key=True)
    codigo_orgao = db.Column(db.String(255), primary_key=True)
    
    # FIELDS: 30 caracteres máximo, obrigatório
    descricao = db.Column(db.String(30), nullable=False)
    
    # OPTIONAL: S ou N (FNDE indicator)
    ind_fnde = db.Column(db.String(1))
    
    # AUDIT FIELDS: auto timestamp
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    data_modificacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships - NOTE: backref='contas' is defined in CONTA_CLASSIFICADA.fonte relationship
    
    def __repr__(self):
        return f'<FONTE_RECURSOS {self.codigo_fonte}-{self.codigo_orgao}>'
    
    def to_dict(self):
        """
        Convert to dictionary for audit trail and API responses
        Includes ALL fields for complete audit coverage
        """
        return {
            'codigo_fonte': self.codigo_fonte,
            'codigo_orgao': self.codigo_orgao,
            'descricao': self.descricao,
            'ind_fnde': self.ind_fnde,
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None,
            'data_modificacao': self.data_modificacao.isoformat() if self.data_modificacao else None,
        }
