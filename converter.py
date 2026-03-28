#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import csv

# Adicionar o caminho ao sys.path para evitar conflito com json.py local
sys.path.insert(0, 'C:\\Users\\Pedro\\OneDrive\\Área de Trabalho\\assessing-examinations-llm')

# Agora importar json
import json as json_module

def converter_dataset():
    """
    Converte dataset.json para CSV com o seguinte formato:
    ID, enunciado, opcao, texto_alternativa, resposta (0 ou 1)
    """
    
    # Caminho dos arquivos
    json_path = 'src/dataset/dataset.json'
    csv_path = 'src/dataset/questoes.csv'
    
    # Ler o JSON
    with open(json_path, 'r', encoding='utf-8') as f:
        dados = json_module.load(f)
    
    # Criar o CSV
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['id', 'enunciado', 'opcao', 'texto_alternativa', 'resposta']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        # Processar cada questão
        for questao in dados:
            questao_id = questao['id']
            enunciado = questao['pergunta']
            resposta_correta = questao['correta']
            alternativas = questao['alternativas']
            
            # Escrever uma linha para cada alternativa
            for opcao, texto in alternativas.items():
                resposta = 1 if opcao == resposta_correta else 0
                
                writer.writerow({
                    'id': questao_id,
                    'enunciado': enunciado,
                    'opcao': opcao,
                    'texto_alternativa': texto,
                    'resposta': resposta
                })
    
    print(f"✓ CSV criado com sucesso em: {csv_path}")
    print(f"✓ Total de questões processadas: {len(dados)}")
    print(f"✓ Total de linhas no CSV: {len(dados) * 5}")  # 5 alternativas por questão

if __name__ == "__main__":
    os.chdir('C:\\Users\\Pedro\\OneDrive\\Área de Trabalho\\assessing-examinations-llm')
    converter_dataset()
