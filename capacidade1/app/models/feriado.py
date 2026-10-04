# -*- coding: utf-8 -*-
"""
FERIADO_ORGAO model - Holidays (C192T)
Funcionalidade F-008: Manter Feriados do Órgão (consolidado com F-015 C806T)
"""

from datetime import datetime
from app import db

class FERIADO_ORGAO(db.Model):
    """
    Public holidays by organizational unit (FERIADO_ORGAO)
    
    Especificação C192T/C806T:
    - Chave Composta: (data, codigo_orgao, tipo_orgao)
    - Data: 8 dígitos (DDMMYYYY, 1994-2099)
    - Código Órgão: por órgão em sessão
    - Tipo Órgão: por tipo órgão em sessão
    - Descrição: 40 caracteres (obrigatória)
    - Creche: S ou N (opcional)
    - Recesso Literal: "RECESSO" ou "RECESSO ESCOLAR" ou null
    - Operações: CON, I, A, E
    - Validação: Data deve ser válida (1994-2099)
    - Paginação: 14 linhas
    - Nota: Consolidado F-008 (C192T) + F-015 (C806T)
    """
    __tablename__ = 'feriado_orgao'
    
    # COMPOSITE PRIMARY KEY: (data, codigo_orgao, tipo_orgao)
    data = db.Column(db.Date, primary_key=True)
    codigo_orgao = db.Column(db.String(255), primary_key=True)
    tipo_orgao = db.Column(db.String(255), primary_key=True)
    
    # FIELDS: 40 caracteres máximo, obrigatório
    descricao = db.Column(db.String(40), nullable=False)
    
    # OPTIONAL: S ou N (creche indicator)
    creche = db.Column(db.String(1))
    
    # OPTIONAL: "RECESSO" ou "RECESSO ESCOLAR" ou null
    recesso_literal = db.Column(db.String(255))
    
    # AUDIT FIELDS: auto timestamp
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    data_modificacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<FERIADO_ORGAO {self.data}-{self.codigo_orgao}-{self.tipo_orgao}>'
    
    def to_dict(self):
        """
        Convert to dictionary for audit trail and API responses
        Includes ALL fields for complete audit coverage
        """
        return {
            'data': self.data.isoformat() if self.data else None,
            'codigo_orgao': self.codigo_orgao,
            'tipo_orgao': self.tipo_orgao,
            'descricao': self.descricao,
            'creche': self.creche,
            'recesso_literal': self.recesso_literal,
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None,
            'data_modificacao': self.data_modificacao.isoformat() if self.data_modificacao else None,
        }
