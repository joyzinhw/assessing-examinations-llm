#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import csv
import os

def limpar_texto(texto):
    """Remove quebras de linha e espaços extras"""
    return ' '.join(texto.split())

def extrair_questoes_txt_v2():
    """
    Extrai questões do arquivo TXT e cria um CSV estruturado com encoding correto
    """
    
    txt_path = 'src/dataset/dataset_pc2025.txt'
    csv_path = 'src/dataset/questoes.csv'
    
    # Ler o arquivo TXT com encoding correto
    with open(txt_path, 'r', encoding='utf-8') as f:
        linhas = f.readlines()
    
    questoes_dict = {}
    codigo_atual = None
    i = 0
    
    while i < len(linhas):
        linha = linhas[i].strip()
        
        # Procurar por "Código: pc2025_XX_YY"
        if linha.startswith('Código:'):
            match = re.search(r'Código:\s+(pc\d+_\d+_\w+)', linha)
            if match:
                codigo_atual = match.group(1)
            i += 1
            continue
        
        # Procurar por número de questão (número sozinho em uma linha)
        if codigo_atual and linha and linha.isdigit():
            numero_questao = linha
            i += 1
            
            # Coletar o enunciado (linhas até encontrar "(A)")
            enunciado_linhas = []
            while i < len(linhas):
                linha_atual = linhas[i].rstrip()
                if linha_atual.strip().startswith('(A)'):
                    break
                if linha_atual.strip():
                    enunciado_linhas.append(linha_atual)
                i += 1
            
            enunciado = limpar_texto(' '.join(enunciado_linhas))
            
            # Coletar as alternativas
            alternativas = {}
            while i < len(linhas):
                linha_alt = linhas[i].rstrip()
                
                # Procurar por padrão "(X) texto"
                match_alt = re.match(r'\(([A-E])\)\s+(.*)', linha_alt)
                if match_alt:
                    opcao = match_alt.group(1)
                    texto_alt = match_alt.group(2)
                    
                    # Coletar as linhas seguintes até a próxima alternativa ou fim
                    i += 1
                    while i < len(linhas):
                        linha_prox = linhas[i].rstrip()
                        # Verificar se é nova alternativa ou novo número de questão
                        if re.match(r'\([A-E]\)\s+', linha_prox) or (linha_prox.strip() and linha_prox.strip().isdigit()):
                            break
                        if linha_prox.strip():
                            texto_alt += ' ' + linha_prox
                        i += 1
                    
                    alternativas[opcao] = limpar_texto(texto_alt)
                else:
                    # Se não é alternativa e não é vazio, pode ser nova questão
                    if linha_alt.strip() and not re.match(r'\(', linha_alt.strip()):
                        i += 1
                    else:
                        break
            
            # Salvar a questão se tiver alternativas
            if alternativas and len(alternativas) == 5:
                questao_id = f"{codigo_atual}_{numero_questao}"
                questoes_dict[questao_id] = {
                    'enunciado': enunciado,
                    'alternativas': alternativas
                }
            continue
        
        i += 1
    
    # Criar o CSV
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['id', 'enunciado', 'opcao', 'texto_alternativa', 'resposta']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        # Processar cada questão
        for questao_id in sorted(questoes_dict.keys()):
            questao = questoes_dict[questao_id]
            enunciado = questao['enunciado']
            alternativas = questao['alternativas']
            
            # Escrever uma linha para cada alternativa
            for opcao in ['A', 'B', 'C', 'D', 'E']:
                if opcao in alternativas:
                    writer.writerow({
                        'id': questao_id,
                        'enunciado': enunciado,
                        'opcao': opcao,
                        'texto_alternativa': alternativas[opcao],
                        'resposta': 0  # Placeholder
                    })
    
    print(f"✓ CSV criado com sucesso em: {csv_path}")
    print(f"✓ Total de questões extraídas: {len(questoes_dict)}")
    print(f"✓ Total de linhas no CSV: {len(questoes_dict) * 5}")
    print("\n⚠️  Nota: A coluna 'resposta' foi preenchida com 0 (padrão).")
    print("    Informe o gabarito para marcar as respostas corretas com 1.")
    
    return questoes_dict

if __name__ == "__main__":
    os.chdir('C:\\Users\\Pedro\\OneDrive\\Área de Trabalho\\assessing-examinations-llm')
    extrair_questoes_txt_v2()
