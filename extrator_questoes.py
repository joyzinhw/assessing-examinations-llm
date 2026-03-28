#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo para Extração de Questões - Processa arquivos TXT de provas

Este módulo oferece classes e funções para:
1. Ler arquivos TXT com provas
2. Extrair questões, enunciados e alternativas
3. Exportar para CSV estruturado
"""

import re
import csv
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional
from pathlib import Path


@dataclass
class Questao:
    """Representa uma única questão"""
    id: str                              # ID único (ex: pc2025_01_pn_31)
    codigo_prova: str                    # Código da prova (ex: pc2025_01_pn)
    numero: str                          # Número da questão (ex: 31)
    enunciado: str                       # Texto da questão
    alternativas: Dict[str, str]         # Dict com chaves A-E e textos das alternativas


class ExtratorQuestoesTXT:
    """
    Extrai questões de um arquivo TXT de prova
    
    Exemplo:
        >>> extrator = ExtratorQuestoesTXT('src/dataset/dataset_pc2025.txt')
        >>> questoes = extrator.extrair()
        >>> print(f"Total de questões: {len(questoes)}")
    """
    
    def __init__(self, caminho_arquivo: str):
        """
        Inicializa o extrator
        
        Args:
            caminho_arquivo: Caminho completo ou relativo do arquivo TXT
        """
        self.caminho = Path(caminho_arquivo)
        if not self.caminho.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {self.caminho}")
        
        self.questoes: List[Questao] = []
    
    def extrair(self) -> List[Questao]:
        """
        Extrai todas as questões do arquivo
        
        Returns:
            Lista de objetos Questao
        """
        print(f"📖 Lendo arquivo: {self.caminho.name}")
        
        with open(self.caminho, 'r', encoding='utf-8') as f:
            conteudo = f.read()
        
        # Dividir por seções de código (Código: pc2025_XX_YY)
        blocos = re.split(r'(?=Código:)', conteudo)
        
        for bloco in blocos:
            self._processar_bloco(bloco)
        
        print(f"✓ {len(self.questoes)} questões extraídas")
        return self.questoes
    
    def _processar_bloco(self, bloco: str) -> None:
        """
        Processa um bloco de prova (um código específico)
        
        Args:
            bloco: Texto contendo um código de prova e suas questões
        """
        # Encontrar o código da prova
        match_codigo = re.search(r'Código:\s+([\w\d_]+)', bloco)
        if not match_codigo:
            return
        
        codigo_prova = match_codigo.group(1)
        
        # Remover cabeçalho
        bloco_limpo = re.sub(r'^.*?Código:.*?\n', '', bloco, count=1, flags=re.DOTALL)
        
        # Encontrar todas as questões (começam com dois dígitos)
        for match in re.finditer(r'\n(\d{2})\n', bloco_limpo):
            self._processar_questao(
                bloco_limpo,
                match,
                codigo_prova
            )
    
    def _processar_questao(self, texto: str, match_num: re.Match, codigo_prova: str) -> None:
        """
        Extrai uma questão específica
        
        Args:
            texto: Texto completo do bloco
            match_num: Match do número da questão
            codigo_prova: Código da prova (ex: pc2025_01_pn)
        """
        numero_questao = match_num.group(1)
        pos_inicio = match_num.start()
        
        # Encontrar o final da questão (próximo número de dois dígitos ou fim)
        matches_prox = list(re.finditer(r'\n\d{2}\n', texto))
        idx_atual = next(
            (i for i, m in enumerate(matches_prox) if m.start() >= pos_inicio),
            -1
        )
        
        if idx_atual >= 0 and idx_atual < len(matches_prox) - 1:
            pos_final = matches_prox[idx_atual + 1].start()
            texto_questao = texto[pos_inicio:pos_final]
        else:
            texto_questao = texto[pos_inicio:]
        
        # Extrair enunciado
        match_enunci = re.search(r'\n\(A\)', texto_questao)
        if not match_enunci:
            return
        
        enunciado = texto_questao[:match_enunci.start()].strip()
        enunciado = re.sub(r'^\d+\s*\n', '', enunciado).strip()
        enunciado = ' '.join(enunciado.split())  # Limpar espaços
        
        # Extrair alternativas
        alternativas = self._extrair_alternativas(texto_questao)
        
        if len(alternativas) == 5:
            questao = Questao(
                id=f"{codigo_prova}_{numero_questao}",
                codigo_prova=codigo_prova,
                numero=numero_questao,
                enunciado=enunciado,
                alternativas=alternativas
            )
            self.questoes.append(questao)
    
    def _extrair_alternativas(self, texto: str) -> Dict[str, str]:
        """
        Extrai as 5 alternativas de uma questão
        
        Args:
            texto: Texto contendo as alternativas
        
        Returns:
            Dicionário com chaves A-E e textos das alternativas
        """
        alternativas = {}
        
        for opcao in ['A', 'B', 'C', 'D', 'E']:
            # Procurar padrão "(X) texto"
            padrao = rf'\({opcao}\)\s+(.*?)(?=\n\(|$)'
            match = re.search(padrao, texto, re.DOTALL)
            
            if match:
                texto_alt = match.group(1)
                # Limpar quebras de linha e espaços múltiplos
                texto_alt = ' '.join(texto_alt.split())
                alternativas[opcao] = texto_alt
        
        return alternativas
    
    def para_csv(self, caminho_saida: str) -> None:
        """
        Exporta as questões para um arquivo CSV
        
        Args:
            caminho_saida: Caminho do arquivo CSV de saída
        """
        if not self.questoes:
            print("⚠️  Nenhuma questão extraída. Execute extrair() primeiro.")
            return
        
        caminho = Path(caminho_saida)
        caminho.parent.mkdir(parents=True, exist_ok=True)
        
        print(f"💾 Salvando em: {caminho.name}")
        
        with open(caminho, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            
            # Cabeçalho
            writer.writerow(['id', 'enunciado', 'opcao', 'texto_alternativa', 'resposta'])
            
            # Escrever uma linha para cada alternativa
            for questao in self.questoes:
                for opcao in ['A', 'B', 'C', 'D', 'E']:
                    writer.writerow([
                        questao.id,
                        questao.enunciado,
                        opcao,
                        questao.alternativas[opcao],
                        0  # Resposta padrão (será atualizada depois)
                    ])
        
        total_linhas = len(self.questoes) * 5
        print(f"✓ {len(self.questoes)} questões exportadas ({total_linhas} linhas)")
