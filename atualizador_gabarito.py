#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo para Atualizar Gabarito - Marca as respostas corretas no CSV

Este módulo permite:
1. Ler um arquivo de gabarito (texto simples)
2. Atualizar o CSV com as respostas corretas
3. Validar integridade dos dados
"""

import csv
from pathlib import Path
from typing import Dict, Tuple
from collections import defaultdict


class AtualizadorGabarito:
    """
    Atualiza as respostas corretas em um CSV de questões
    
    Exemplo:
        >>> atualizador = AtualizadorGabarito('src/dataset/questoes_pc2025.csv')
        >>> atualizador.carregar_gabarito('gabarito_pc2025.txt')
        >>> atualizador.atualizar()
    """
    
    def __init__(self, caminho_csv: str):
        """
        Inicializa o atualizador
        
        Args:
            caminho_csv: Caminho do arquivo CSV a atualizar
        """
        self.caminho_csv = Path(caminho_csv)
        if not self.caminho_csv.exists():
            raise FileNotFoundError(f"Arquivo CSV não encontrado: {self.caminho_csv}")
        
        self.gabarito: Dict[str, str] = {}  # ID da questão -> resposta (A-E)
        self.linhas_csv = []
    
    def carregar_gabarito(self, caminho_gabarito: str) -> None:
        """
        Carrega o gabarito de um arquivo de texto
        
        Formato esperado do arquivo:
            pc2025_01_pn_31:C
            pc2025_01_pn_32:E
            pc2025_01_pn_33:B
            ...
        
        Args:
            caminho_gabarito: Caminho do arquivo de gabarito
        
        Raises:
            FileNotFoundError: Se o arquivo não existir
            ValueError: Se o formato do arquivo estiver incorreto
        """
        caminho = Path(caminho_gabarito)
        
        if not caminho.exists():
            raise FileNotFoundError(f"Arquivo de gabarito não encontrado: {caminho}")
        
        print(f"📖 Carregando gabarito: {caminho.name}")
        
        linhas_validas = 0
        linhas_invalidas = 0
        
        with open(caminho, 'r', encoding='utf-8') as f:
            for num_linha, linha in enumerate(f, 1):
                linha = linha.strip()
                
                # Pular linhas vazias ou comentários
                if not linha or linha.startswith('#'):
                    continue
                
                # Parsear formato ID:RESPOSTA
                if ':' not in linha:
                    print(f"  ⚠️  Linha {num_linha} com formato inválido: {linha}")
                    linhas_invalidas += 1
                    continue
                
                partes = linha.split(':')
                if len(partes) != 2:
                    print(f"  ⚠️  Linha {num_linha} com formato inválido: {linha}")
                    linhas_invalidas += 1
                    continue
                
                questao_id = partes[0].strip()
                resposta = partes[1].strip().upper()
                
                # Validar resposta
                if resposta not in ['A', 'B', 'C', 'D', 'E']:
                    print(f"  ⚠️  Linha {num_linha}: resposta inválida '{resposta}'")
                    linhas_invalidas += 1
                    continue
                
                self.gabarito[questao_id] = resposta
                linhas_validas += 1
        
        print(f"✓ {linhas_validas} entradas carregadas")
        if linhas_invalidas > 0:
            print(f"  ⚠️  {linhas_invalidas} linhas ignoradas")
    
    def carregar_csv(self) -> None:
        """Carrega o CSV para memória"""
        print(f"📖 Lendo CSV: {self.caminho_csv.name}")
        
        with open(self.caminho_csv, 'r', encoding='utf-8-sig') as f:
            leitor = csv.DictReader(f)
            self.linhas_csv = list(leitor)
        
        print(f"✓ {len(self.linhas_csv)} linhas carregadas")
    
    def atualizar(self) -> Tuple[int, int]:
        """
        Atualiza as respostas corretas no CSV
        
        Returns:
            Tupla (linhas_atualizadas, linhas_nao_encontradas)
        """
        if not self.gabarito:
            print("⚠️  Nenhum gabarito carregado. Execute carregar_gabarito() primeiro.")
            return 0, 0
        
        if not self.linhas_csv:
            self.carregar_csv()
        
        # Mapear questões únicas
        questoes_uniques = {}
        for linha in self.linhas_csv:
            questao_id = linha['id']
            if questao_id not in questoes_uniques:
                questoes_uniques[questao_id] = {
                    'encontrada': questao_id in self.gabarito,
                    'resposta_correta': self.gabarito.get(questao_id, '')
                }
        
        # Atualizar respostas
        print("\n✏️  Atualizando respostas...")
        atualizadas = 0
        nao_encontradas = 0
        
        for linha in self.linhas_csv:
            questao_id = linha['id']
            
            if questao_id in self.gabarito:
                resposta_correta = self.gabarito[questao_id]
                # Marcar com 1 se for a resposta correta, 0 caso contrário
                linha['resposta'] = '1' if linha['opcao'] == resposta_correta else '0'
                atualizadas += 1
            else:
                nao_encontradas += 1
        
        # Salvar CSV atualizado
        print(f"💾 Salvando CSV: {self.caminho_csv.name}")
        
        with open(self.caminho_csv, 'w', newline='', encoding='utf-8-sig') as f:
            fieldnames = ['id', 'enunciado', 'opcao', 'texto_alternativa', 'resposta']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.linhas_csv)
        
        print(f"✓ {atualizadas} respostas atualizadas")
        
        if nao_encontradas > 0:
            print(f"⚠️  {nao_encontradas} linhas sem gabarito correspondente")
        
        return atualizadas, nao_encontradas
    
    def gerar_relatorio(self) -> None:
        """Gera um relatório de quais questões tiveram gabarito"""
        if not self.linhas_csv:
            self.carregar_csv()
        
        questoes_unicas = set(linha['id'] for linha in self.linhas_csv)
        com_gabarito = len([q for q in questoes_unicas if q in self.gabarito])
        sem_gabarito = len(questoes_unicas) - com_gabarito
        
        print("\n📊 Relatório de Gabarito:")
        print(f"  Total de questões: {len(questoes_unicas)}")
        print(f"  Com gabarito: {com_gabarito}")
        print(f"  Sem gabarito: {sem_gabarito}")
        
        if sem_gabarito > 0:
            print(f"\n  Questões sem gabarito:")
            for questao_id in sorted(questoes_unicas):
                if questao_id not in self.gabarito:
                    print(f"    • {questao_id}")
