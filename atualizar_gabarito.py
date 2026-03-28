#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para atualizar as respostas corretas no CSV

Exemplo de uso:
    python atualizar_gabarito.py

O gabarito deve ser fornecido no formato:
    id_questao:resposta_correta

Exemplo:
    pc2025_01_pn_31:C
    pc2025_01_pn_32:E
    pc2025_01_pn_33:B
    ...
"""

import csv
from pathlib import Path
from collections import defaultdict

def atualizar_gabarito_interativo():
    """
    Permite atualizar o gabarito das questões de forma interativa
    """
    
    csv_path = Path('src/dataset/questoes.csv')
    
    print("=" * 70)
    print("ATUALIZADOR DE GABARITO - QUESTÕES")
    print("=" * 70)
    print()
    print("Digite o gabarito no formato: ID_QUESTAO:RESPOSTA")
    print("Exemplo: pc2025_01_pn_31:C")
    print()
    print("Ou carregue de um arquivo (pressure 'f' e enter para carregar arquivo)")
    print("Ou digite 'sair' para terminar")
    print()
    
    gabarito = defaultdict(str)
    
    while True:
        entrada = input(">> ").strip()
        
        if entrada.lower() == 'sair':
            break
        elif entrada.lower() == 'f':
            arquivo = input("Nome do arquivo com o gabarito: ").strip()
            try:
                with open(arquivo, 'r', encoding='utf-8') as f:
                    for linha in f:
                        linha = linha.strip()
                        if ':' in linha:
                            qid, resp = linha.split(':')
                            gabarito[qid.strip()] = resp.strip().upper()
                print(f"✓ {len(gabarito)} respostas carregadas do arquivo")
            except FileNotFoundError:
                print("✗ Arquivo não encontrado")
        elif ':' in entrada:
            qid, resp = entrada.split(':')
            qid = qid.strip()
            resp = resp.strip().upper()
            if resp in ['A', 'B', 'C', 'D', 'E']:
                gabarito[qid] = resp
                print(f"✓ {qid} = {resp}")
            else:
                print("✗ Resposta inválida (deve ser A, B, C, D ou E)")
        else:
            print("✗ Formato inválido. Use: ID:RESPOSTA")
    
    # Atualizar o CSV
    if not gabarito:
        print("\nNenhuma resposta foi informada. Abortando.")
        return
    
    print(f"\nAtualizando {len(gabarito)} questões no CSV...")
    
    linhas = []
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        leitor = csv.DictReader(f)
        for linha in leitor:
            questao_id = linha['id']
            if questao_id in gabarito:
                resposta_correta = gabarito[questao_id]
                linha['resposta'] = '1' if linha['opcao'] == resposta_correta else '0'
            linhas.append(linha)
    
    # Reescrever o CSV
    with open(csv_path, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'enunciado', 'opcao', 'texto_alternativa', 'resposta'])
        writer.writeheader()
        writer.writerows(linhas)
    
    print(f"✓ CSV atualizado com sucesso!")
    print(f"  Arquivo: {csv_path}")

if __name__ == "__main__":
    atualizar_gabarito_interativo()
