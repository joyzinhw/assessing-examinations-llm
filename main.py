#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script Principal - Orquestra a extração e atualização de questões

Este script fornece uma interface simple para:
1. Extrair questões de arquivos TXT
2. Atualizar gabarito
3. Listar provas disponíveis

Uso:
    python main.py extrair pc2025
    python main.py gabarito pc2025 gabarito_pc2025.txt
    python main.py listar
"""

import sys
from pathlib import Path

# Importar módulos do projeto
from config_provas import obter_config_prova, listar_provas_disponiveis, PROVAS_DISPONIVEIS
from extrator_questoes import ExtratorQuestoesTXT
from atualizador_gabarito import AtualizadorGabarito


def extrair_questoes(tipo_prova: str) -> None:
    """
    Extrai questões de um arquivo TXT de prova
    
    Args:
        tipo_prova: Tipo de prova (ex: 'pc2025', 'pm2025')
    """
    try:
        config = obter_config_prova(tipo_prova)
        
        print(f"\n{'='*60}")
        print(f"🎯 Extraindo: {config.descricao}")
        print(f"{'='*60}\n")
        
        # Caminhos completos
        caminho_entrada = f"src/dataset/{config.arquivo_entrada}"
        caminho_saida = f"src/dataset/{config.arquivo_saida}"
        
        # Verificar se arquivo de entrada existe
        if not Path(caminho_entrada).exists():
            print(f"❌ Arquivo não encontrado: {caminho_entrada}")
            print(f"   Por favor, adicione o arquivo '{config.arquivo_entrada}' em 'src/dataset/'")
            return
        
        # Extrair questões
        extrator = ExtratorQuestoesTXT(caminho_entrada)
        questoes = extrator.extrair()
        
        if questoes:
            # Exportar para CSV
            extrator.para_csv(caminho_saida)
            print(f"\n✨ Extração concluída com sucesso!")
            print(f"   Arquivo salvo: {caminho_saida}")
        else:
            print(f"\n⚠️  Nenhuma questão foi extraída")
            print(f"   Verifique o formato do arquivo '{config.arquivo_entrada}'")
    
    except ValueError as e:
        print(f"❌ Erro: {e}")
        listar_provas_disponiveis()
    except Exception as e:
        print(f"❌ Erro durante a execução: {e}")


def atualizar_gabarito(tipo_prova: str, arquivo_gabarito: str) -> None:
    """
    Atualiza o gabarito em um CSV de questões
    
    Args:
        tipo_prova: Tipo de prova (ex: 'pc2025')
        arquivo_gabarito: Caminho do arquivo com o gabarito
    """
    try:
        config = obter_config_prova(tipo_prova)
        
        print(f"\n{'='*60}")
        print(f"🎯 Atualizando Gabarito: {config.nome}")
        print(f"{'='*60}\n")
        
        # Caminhos completos
        caminho_csv = f"src/dataset/{config.arquivo_saida}"
        
        # Verificar se arquivo CSV existe
        if not Path(caminho_csv).exists():
            print(f"❌ Arquivo CSV não encontrado: {caminho_csv}")
            print(f"   Execute 'python main.py extrair {tipo_prova}' primeiro")
            return
        
        # Verificar se arquivo de gabarito existe
        if not Path(arquivo_gabarito).exists():
            print(f"❌ Arquivo de gabarito não encontrado: {arquivo_gabarito}")
            print(f"   Crie um arquivo no formato:")
            print(f"      pc2025_01_pn_31:C")
            print(f"      pc2025_01_pn_32:E")
            print(f"      ...")
            return
        
        # Atualizar gabarito
        atualizador = AtualizadorGabarito(caminho_csv)
        atualizador.carregar_gabarito(arquivo_gabarito)
        atualizador.gerar_relatorio()
        
        print()
        atualizador.atualizar()
        
        print(f"\n✨ Gabarito atualizado com sucesso!")
        print(f"   Arquivo: {caminho_csv}")
    
    except ValueError as e:
        print(f"❌ Erro: {e}")
        listar_provas_disponiveis()
    except Exception as e:
        print(f"❌ Erro durante a execução: {e}")


def listar_provas() -> None:
    """Lista todas as provas disponíveis"""
    print(f"\n{'='*60}")
    print("📚 PROVAS DISPONÍVEIS")
    print(f"{'='*60}")
    listar_provas_disponiveis()


def mostrar_ajuda() -> None:
    """Mostra a mensagem de ajuda"""
    print(f"""
{'='*60}
📚 EXTRATOR DE QUESTÕES - Sistema de Gerenciamento de Provas
{'='*60}

COMANDOS DISPONÍVEIS:

  1. Extrair questões de um arquivo TXT
     $ python main.py extrair <tipo_prova>
     
     Exemplo:
     $ python main.py extrair pc2025
     $ python main.py extrair pm2025

  2. Atualizar gabarito das respostas
     $ python main.py gabarito <tipo_prova> <arquivo_gabarito>
     
     Exemplo:
     $ python main.py gabarito pc2025 gabarito_pc2025.txt
     
     O arquivo de gabarito deve estar no formato:
       pc2025_01_pn_31:C
       pc2025_01_pn_32:E
       pc2025_01_pn_33:B
       ...

  3. Listar provas disponíveis
     $ python main.py listar

  4. Mostrar esta ajuda
     $ python main.py ajuda

{'='*60}
ESTRUTURA DE PASTAS ESPERADA:

  src/dataset/
    ├── dataset_pc2025.txt      (arquivo de entrada)
    ├── questoes_pc2025.csv     (arquivo de saída gerado)
    ├── dataset_pm2025.txt      (arquivo de entrada opcional)
    ├── questoes_pm2025.csv     (arquivo de saída gerado)
    └── gabarito_pc2025.txt     (arquivo com respostas corretas)

{'='*60}
PROCESSO RECOMENDADO:

  1. Coloque o arquivo TXT em src/dataset/
  2. Configure a prova em config_provas.py se necessário
  3. Extraia as questões:
     $ python main.py extrair pc2025
  4. Crie um arquivo de gabarito em src/dataset/gabarito_pc2025.txt
  5. Atualize o gabarito:
     $ python main.py gabarito pc2025 src/dataset/gabarito_pc2025.txt

{'='*60}
""")


def main():
    """Função principal"""
    if len(sys.argv) < 2:
        mostrar_ajuda()
        return
    
    comando = sys.argv[1].lower()
    
    if comando == 'extrair':
        if len(sys.argv) < 3:
            print("❌ Erro: tipo de prova não especificado")
            print("   Uso: python main.py extrair <tipo_prova>")
            listar_provas_disponiveis()
            return
        tipo_prova = sys.argv[2]
        extrair_questoes(tipo_prova)
    
    elif comando == 'gabarito':
        if len(sys.argv) < 4:
            print("❌ Erro: tipo de prova ou arquivo de gabarito não especificado")
            print("   Uso: python main.py gabarito <tipo_prova> <arquivo_gabarito>")
            return
        tipo_prova = sys.argv[2]
        arquivo_gabarito = sys.argv[3]
        atualizar_gabarito(tipo_prova, arquivo_gabarito)
    
    elif comando == 'listar':
        listar_provas()
    
    elif comando in ['ajuda', 'help', '-h', '--help']:
        mostrar_ajuda()
    
    else:
        print(f"❌ Comando desconhecido: '{comando}'")
        mostrar_ajuda()


if __name__ == "__main__":
    main()
