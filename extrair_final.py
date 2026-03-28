#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import csv
from pathlib import Path

def extrair_questoes_final():
    """
    Extrai questões do arquivo TXT com parsing robusto
    """
    
    txt_path = Path('src/dataset/dataset_pc2025.txt')
    csv_path = Path('src/dataset/questoes.csv')
    
    with open(txt_path, 'r', encoding='utf-8') as f:
        texto = f.read()
    
    # Dividir por seções de "Código:"
    # Primeiro, encontrar todos os blocos por código
    blocos = re.split(r'(?=Código:)', texto)
    
    questoes = []
    
    for bloco in blocos:
        # Extrair código
        match_codigo = re.search(r'Código:\s+(pc\d+_\d+_\w+)', bloco)
        if not match_codigo:
            continue
            
        codigo = match_codigo.group(1)
        
        # Remover o código e partes de cabeçalho
        bloco_limpo = re.sub(r'^.*?Código:.*?\n', '', bloco, count=1, flags=re.DOTALL)
        
        # Padrão para encontrar questões:
        # - Começa com número inteiro (a questão)
        # - Seguido pelo enunciado
        # - Seguido pelas 5 alternativas (A) até (E)
        pattern_questao = r'(\d+)\n(.*?)(?=\n[A-E]\)|$)'
        
        # Encontrar números de questões
        for match in re.finditer(r'\n(\d{2})\n', bloco_limpo):
            pos_num = match.start()
            num_questao = match.group(1)
            
            # Encontrar o final da questão (próximo número ou fim)
            matches_prox = list(re.finditer(r'\n[0-9]{2}\n', bloco_limpo))
            idx_atual = matches_prox.index(match) if match in matches_prox else -1
            
            if idx_atual >= 0 and idx_atual < len(matches_prox) - 1:
                pos_final = matches_prox[idx_atual + 1].start()
                texto_questao = bloco_limpo[pos_num:pos_final]
            else:
                texto_questao = bloco_limpo[pos_num:]
            
            # Extrair enunciado (até primeira alternativa)
            match_enum = re.search(r'\n\(A\)', texto_questao)
            if match_enum:
                enunciado_texto = texto_questao[:match_enum.start()].strip()
                # Remover número da questão
                enunciado_texto = re.sub(r'^\d+\s*\n', '', enunciado_texto).strip()
                # Limpar quebras de linha e espaços múltiplos
                enunciado_texto = ' '.join(enunciado_texto.split())
                
                # Extrair alternativas
                alternativas = {}
                for opcao in ['A', 'B', 'C', 'D', 'E']:
                    pat_alt = rf'\({opcao}\)\s+(.*?)(?=\n\(|$)'
                    match_alt = re.search(pat_alt, texto_questao, re.DOTALL)
                    if match_alt:
                        texto_alt = ' '.join(match_alt.group(1).split())
                        # Remover partes de orientação
                        texto_alt = texto_alt.split('(')[0].strip() if '(' in texto_alt else texto_alt
                        alternativas[opcao] = texto_alt
                
                if len(alternativas) == 5:
                    questoes.append({
                        'id': f"{codigo}_{num_questao}",
                        'enunciado': enunciado_texto,
                        'alternativas': alternativas
                    })
    
    # Salvar CSV
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(['id', 'enunciado', 'opcao', 'texto_alternativa', 'resposta'])
        
        for q in questoes:
            for opcao in ['A', 'B', 'C', 'D', 'E']:
                writer.writerow([
                    q['id'],
                    q['enunciado'],
                    opcao,
                    q['alternativas'][opcao],
                    0
                ])
    
    print(f"✓ CSV criado: {csv_path}")
    print(f"✓ Questões extraídas: {len(questoes)}")
    print(f"✓ Linhas no CSV: {len(questoes) * 5}")

if __name__ == "__main__":
    extrair_questoes_final()
