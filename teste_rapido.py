#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de Teste Rápido - Valida se o sistema está funcionando

Executa testes básicos para verificar se:
1. Todos os módulos podem ser importados
2. Configurações estão corretas
3. Arquivos estão no lugar certo
4. Sistema está pronto para uso
"""

import sys
from pathlib import Path

def teste_imports():
    """Testa se todos os módulos podem ser importados"""
    print("🔍 Testando imports...")
    try:
        from config_provas import obter_config_prova, PROVAS_DISPONIVEIS
        print("  ✅ config_provas")
        
        from extrator_questoes import ExtratorQuestoesTXT, Questao
        print("  ✅ extrator_questoes")
        
        from atualizador_gabarito import AtualizadorGabarito
        print("  ✅ atualizador_gabarito")
        
        return True
    except ImportError as e:
        print(f"  ❌ Erro ao importar: {e}")
        return False

def teste_estrutura_pastas():
    """Testa se pastas necessárias existem"""
    print("\n🔍 Testando estrutura de pastas...")
    
    pastas_necessarias = [
        'src',
        'src/dataset',
    ]
    
    todas_ok = True
    for pasta in pastas_necessarias:
        if Path(pasta).exists():
            print(f"  ✅ {pasta}/")
        else:
            print(f"  ❌ {pasta}/ (não existe)")
            todas_ok = False
    
    return todas_ok

def teste_arquivos():
    """Testa se arquivos principais existem"""
    print("\n🔍 Testando arquivos...")
    
    arquivos_necessarios = [
        'main.py',
        'config_provas.py',
        'extrator_questoes.py',
        'atualizador_gabarito.py',
        'gerar_gabarito_exemplo.py',
    ]
    
    todas_ok = True
    for arquivo in arquivos_necessarios:
        if Path(arquivo).exists():
            print(f"  ✅ {arquivo}")
        else:
            print(f"  ❌ {arquivo} (não existe)")
            todas_ok = False
    
    return todas_ok

def teste_arquivo_entrada():
    """Testa se arquivo de entrada existe"""
    print("\n🔍 Testando arquivo de entrada...")
    
    arquivo = Path('src/dataset/dataset_pc2025.txt')
    
    if arquivo.exists():
        tamanho = arquivo.stat().st_size
        if tamanho > 0:
            print(f"  ✅ dataset_pc2025.txt ({tamanho:,} bytes)")
            return True
        else:
            print(f"  ❌ dataset_pc2025.txt (vazio)")
            return False
    else:
        print(f"  ❌ dataset_pc2025.txt (não encontrado)")
        print(f"     Coloque arquivo em: src/dataset/dataset_pc2025.txt")
        return False

def teste_provas_config():
    """Testa se ProVAs estão configuradas"""
    print("\n🔍 Testando configuração de provas...")
    
    try:
        from config_provas import PROVAS_DISPONIVEIS
        
        if PROVAS_DISPONIVEIS:
            for tipo, config in PROVAS_DISPONIVEIS.items():
                print(f"  ✅ {config.nome} ({tipo})")
            return True
        else:
            print(f"  ❌ Nenhuma prova configurada")
            return False
    except Exception as e:
        print(f"  ❌ Erro ao carregar provas: {e}")
        return False

def teste_cli():
    """Testa interface CLI"""
    print("\n🔍 Testando interface CLI...")
    
    try:
        # Este teste está simplificado pois main() requer sys.argv
        import main
        print(f"  ✅ CLI está importável e funcional")
        return True
    except Exception as e:
        print(f"  ❌ Erro na CLI: {e}")
        return False

def main():
    """Executa todos os testes"""
    print("=" * 60)
    print("🧪 TESTE RÁPIDO DO SISTEMA")
    print("=" * 60)
    
    resultados = []
    
    # Executar testes
    resultados.append(("Imports", teste_imports()))
    resultados.append(("Estrutura de Pastas", teste_estrutura_pastas()))
    resultados.append(("Arquivos", teste_arquivos()))
    resultados.append(("Arquivo de Entrada", teste_arquivo_entrada()))
    resultados.append(("Configuração de Provas", teste_provas_config()))
    resultados.append(("Interface CLI", teste_cli()))
    
    # Resumo
    print("\n" + "=" * 60)
    print("📊 RESUMO DOS TESTES")
    print("=" * 60)
    
    total = len(resultados)
    passou = sum(1 for _, resultado in resultados if resultado)
    falhou = total - passou
    
    for teste, resultado in resultados:
        status = "✅ PASSAR" if resultado else "❌ FALHAR"
        print(f"{status:12} {teste}")
    
    print("-" * 60)
    print(f"Total: {passou}/{total} testes passaram")
    
    # Status final
    print("=" * 60)
    if falhou == 0:
        print("✅ SISTEMA ESTÁ OK - Pronto para usar!")
        print("\nPróximos passos:")
        print("  1. python main.py listar")
        print("  2. python main.py extrair pc2025")
        print("  3. python gerar_gabarito_exemplo.py")
        return 0
    else:
        print(f"❌ {falhou} teste(s) falharam - Verifique acima")
        print("\nO que fazer:")
        print("  1. Leia as mensagens de erro acima")
        print("  2. Crie pastas faltantes (mkdir src/dataset)")
        print("  3. Coloque arquivo TXT em src/dataset/")
        print("  4. Execute este teste novamente")
        return 1

if __name__ == "__main__":
    sys.exit(main())
