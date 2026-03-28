#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Gera um arquivo de exemplo de gabarito

Use este script para criar um arquivo de gabarito template.
"""

from pathlib import Path

def gerar_exemplo_gabarito():
    """Gera um arquivo de exemplo de gabarito"""
    
    exemplo = """# Arquivo de Gabarito - Formato simples
# 
# Formato: ID_QUESTAO:RESPOSTA_CORRETA
# As linhas começando com '#' são ignoradas
# Deixe em branco para questões sem gabarito

# ===========================================
# DIREITO PENAL (pn)
# ===========================================

pc2025_01_pn_31:C
pc2025_01_pn_32:E
pc2025_01_pn_33:B
pc2025_01_pn_34:D
pc2025_01_pn_35:C
pc2025_01_pn_36:A
pc2025_01_pn_37:E
pc2025_01_pn_38:B

# ===========================================
# DIREITO PROCESSUAL PENAL (ppn)
# ===========================================

pc2025_01_ppn_41:A
pc2025_01_ppn_42:D
pc2025_01_ppn_43:C
pc2025_01_ppn_44:E
pc2025_01_ppn_45:B

# ===========================================
# DIREITO CONSTITUCIONAL (cn)
# ===========================================

pc2025_01_cn_51:E
pc2025_01_cn_52:A
pc2025_01_cn_53:C
pc2025_01_cn_54:D
pc2025_01_cn_55:B

# ===========================================
# DIREITO ADMINISTRATIVO (adm)
# ===========================================

pc2025_01_adm_57:A
pc2025_01_adm_58:D
pc2025_01_adm_59:E
pc2025_01_adm_60:E
pc2025_01_adm_61:D
pc2025_01_adm_62:B

# ===========================================
# LEGISLAÇÃO INSTITUCIONAL DA POLÍCIA CIVIL (lipc)
# ===========================================

pc2025_01_lipc_63:A
pc2025_01_lipc_64:E
pc2025_01_lipc_65:D
pc2025_01_lipc_66:E

"""
    
    # Salvar no arquivo
    caminho = Path('src/dataset/gabarito_pc2025_exemplo.txt')
    caminho.parent.mkdir(parents=True, exist_ok=True)
    
    with open(caminho, 'w', encoding='utf-8') as f:
        f.write(exemplo)
    
    print(f"✓ Arquivo de exemplo criado: {caminho}")
    print(f"\n📝 Copie este arquivo e substitua os valores pelas respostas corretas.")
    print(f"   Depois execute: python main.py gabarito pc2025 {caminho}")

if __name__ == "__main__":
    gerar_exemplo_gabarito()
