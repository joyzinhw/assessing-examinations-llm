#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Configuração de Provas - Define os diferentes tipos e locais de provas

Adicione novos tipos de provas aqui conforme necessário.
"""

from dataclasses import dataclass
from pathlib import Path

@dataclass
class ConfigProva:
    """Configuração de uma prova específica"""
    nome: str                   # Nome da prova (ex: "PC 2025", "PM 2025")
    codigo_prefixo: str         # Prefixo do código (ex: "pc2025", "pm2025")
    arquivo_entrada: str        # Caminho do arquivo TXT (relativo a src/dataset/)
    arquivo_saida: str          # Caminho do arquivo CSV (relativo a src/dataset/)
    descricao: str              # Descrição para logging

# Mapeamento de provas disponíveis
PROVAS_DISPONIVEIS = {
    'pc2025': ConfigProva(
        nome='Polícia Civil 2025',
        codigo_prefixo='pc2025',
        arquivo_entrada='dataset_pc2025.txt',
        arquivo_saida='questoes_pc2025.csv',
        descricao='Prova de Polícia Civil de 2025'
    ),
    'pm2025': ConfigProva(
        nome='Polícia Militar 2025',
        codigo_prefixo='pm2025',
        arquivo_entrada='dataset_pm2025.txt',
        arquivo_saida='questoes_pm2025.csv',
        descricao='Prova de Polícia Militar de 2025'
    ),
}

def obter_config_prova(tipo_prova: str) -> ConfigProva:
    """
    Obtém a configuração de uma prova específica
    
    Args:
        tipo_prova: Tipo de prova ('pc2025', 'pm2025', etc)
    
    Returns:
        ConfigProva: Configuração da prova
    
    Raises:
        ValueError: Se o tipo de prova não existir
    """
    if tipo_prova not in PROVAS_DISPONIVEIS:
        tipos_validos = ', '.join(PROVAS_DISPONIVEIS.keys())
        raise ValueError(
            f"Tipo de prova '{tipo_prova}' desconhecido.\n"
            f"Tipos válidos: {tipos_validos}"
        )
    return PROVAS_DISPONIVEIS[tipo_prova]

def listar_provas_disponiveis() -> None:
    """Lista todas as provas disponíveis"""
    print("\n📋 Provas Disponíveis:")
    print("-" * 50)
    for tipo, config in PROVAS_DISPONIVEIS.items():
        print(f"  • {config.nome:<30} ({tipo})")
        print(f"    Arquivo: {config.arquivo_entrada}")
    print()
