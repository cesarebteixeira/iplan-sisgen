# -*- coding: utf-8 -*-
"""
Auditoria model - System audit trail
Suporte para auditoria de todas as operações (F-001 a F-012)
"""

from datetime import datetime
from app import db
import json

class AUDITORIA(db.Model):
    """
    Audit log table to track all changes in the system (AUDITORIA)
    
    Suporta rastreamento de:
    - A-001: Auditoria Operações I/A/E (F-001 a F-012)
    - A-002: Rastreamento Propagação (F-003: GRUPO)
    - A-003: Registro Histórico Mudanças (F-011, F-012: HISTORICO)
    """
    __tablename__ = 'auditoria'
    
    # PRIMARY KEY: auto-increment sequence
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # FIELDS: Table name (obrigatório)
    tabela = db.Column(db.String(100), nullable=False)
    
    # FIELDS: Operation type (CREATE, UPDATE, DELETE)
    operacao = db.Column(db.String(20), nullable=False)
    
    # FIELDS: Primary key value(s) (obrigatório)
    chave_primaria = db.Column(db.String(500), nullable=False)
    
    # FIELDS: Previous values (JSON)
    valores_anteriores = db.Column(db.Text)
    
    # FIELDS: New values (JSON)
    valores_novos = db.Column(db.Text)
    
    # AUDIT FIELDS: User who made the change
    usuario = db.Column(db.String(255))
    
    # AUDIT FIELDS: Reason for change
    motivo = db.Column(db.Text)
    
    # AUDIT FIELDS: Source IP
    ip_origem = db.Column(db.String(45))
    
    # AUDIT FIELDS: Operation timestamp
    data_operacao = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<AUDITORIA {self.id} - {self.tabela}.{self.operacao}>'
    
    @staticmethod
    def registrar(tabela, operacao, chave_primaria, valores_novos=None, valores_anteriores=None, usuario=None, motivo=None, ip_origem=None):
        """
        Register an audit entry
        
        Args:
            tabela: Table name
            operacao: Operation type (CREATE, UPDATE, DELETE)
            chave_primaria: Primary key value
            valores_novos: New values dict
            valores_anteriores: Previous values dict
            usuario: User identifier
            motivo: Reason for change
            ip_origem: Source IP
        
        Returns:
            AUDITORIA instance
        """
        auditoria = AUDITORIA(
            tabela=tabela,
            operacao=operacao,
            chave_primaria=str(chave_primaria),
            valores_novos=json.dumps(valores_novos) if valores_novos else None,
            valores_anteriores=json.dumps(valores_anteriores) if valores_anteriores else None,
            usuario=usuario,
            motivo=motivo,
            ip_origem=ip_origem,
            data_operacao=datetime.utcnow()
        )
        return auditoria
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'tabela': self.tabela,
            'operacao': self.operacao,
            'chave_primaria': self.chave_primaria,
            'valores_anteriores': json.loads(self.valores_anteriores) if self.valores_anteriores else None,
            'valores_novos': json.loads(self.valores_novos) if self.valores_novos else None,
            'usuario': self.usuario,
            'motivo': self.motivo,
            'ip_origem': self.ip_origem,
            'data_operacao': self.data_operacao.isoformat() if self.data_operacao else None,
        }
