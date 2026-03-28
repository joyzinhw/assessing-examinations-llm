#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
from pathlib import Path

def corrigir_encoding_csv():
    """
    Corrige o encoding do CSV para UTF-8 BOM (melhor compatibilidade com Excel)
    """
    
    csv_path = Path('src/dataset/questoes.csv')
    
    # Ler o CSV
    linhas = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        linhas = f.readlines()
    
    # Reescrever com UTF-8 BOM
    with open(csv_path, 'w', encoding='utf-8-sig', newline='') as f:
        f.writelines(linhas)
    
    print(f"✓ Codificação do CSV corrigida para UTF-8-BOM")
    print(f"✓ Arquivo: {csv_path}")

if __name__ == "__main__":
    corrigir_encoding_csv()
