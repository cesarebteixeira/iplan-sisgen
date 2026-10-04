#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app import create_app

app = create_app()
print('Aplicacao criada com sucesso')

with app.test_client() as client:
    routes = [
        ('/', 'Inicio'),
        ('/unidade/', 'Unidades'),
        ('/bairro/', 'Bairros'),
        ('/grupo/', 'Grupos'),
        ('/feriado/', 'Feriados'),
        ('/projeto/', 'Projetos'),
        ('/vinculo/', 'Vinculos'),
        ('/conta/', 'Contas'),
        ('/tipo_processo/', 'Tipos de Processo'),
        ('/fonte/', 'Fontes'),
    ]
    
    for route, name in routes:
        try:
            r = client.get(route)
            status = 'OK' if r.status_code == 200 else f'ERRO {r.status_code}'
            print(f'{name:20}: {status}')
        except Exception as e:
            print(f'{name:20}: ERRO - {str(e)[:40]}')
