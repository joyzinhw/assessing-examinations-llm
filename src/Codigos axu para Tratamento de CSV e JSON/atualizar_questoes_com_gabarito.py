import csv
import re
from collections import defaultdict

def extrair_numero_questao(id_questao):
    """Extrai o número da questão do ID (último número após underscore)"""
    match = re.search(r'_(\d+)$', id_questao)
    return int(match.group(1)) if match else None


def atualizar_csv_original(caminho_csv_original, caminho_gabarito):
    """
    Lê o CSV original, adiciona/atualiza as respostas do gabarito e sobrescreve o arquivo original
    """
    gabarito_dict = {}
    
    # Carrega gabarito
    with open(caminho_gabarito, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter=",")
        for linha in reader:
            id_q = linha["id"].strip()
            resposta = linha["resposta"].strip()
            numero = extrair_numero_questao(id_q)
            gabarito_dict[numero] = resposta
            gabarito_dict[id_q] = resposta
    
    print(f"✓ Gabarito carregado: {len(gabarito_dict)} entradas")
    
    linhas_processadas = 0
    respostas_atualizadas = 0
    
    with open(caminho_csv_original, encoding="utf-8-sig") as f_in:
        reader = csv.DictReader(f_in, delimiter=",")
        fieldnames = reader.fieldnames
        linhas = []
        
        for linha in reader:
            linhas_processadas += 1
            id_q = linha["id"].strip()
            numero = extrair_numero_questao(id_q)
            
            # Procura resposta no gabarito
            resposta_gabarito = None
            if numero and numero in gabarito_dict:
                resposta_gabarito = gabarito_dict[numero]
            elif id_q in gabarito_dict:
                resposta_gabarito = gabarito_dict[id_q]
            
            if resposta_gabarito:
                linha["resposta"] = resposta_gabarito
                respostas_atualizadas += 1
            
            linhas.append(linha)
        
        # Sobrescreve o arquivo original
        with open(caminho_csv_original, "w", encoding="utf-8-sig", newline="") as f_out:
            writer = csv.DictWriter(f_out, fieldnames=fieldnames, delimiter=",")
            writer.writeheader()
            writer.writerows(linhas)
    
    # Relatório
    print("\n===== RELATÓRIO =====")
    print(f"Total de linhas processadas: {linhas_processadas}")
    print(f"Respostas atualizadas: {respostas_atualizadas}")
    print(f"✓ Arquivo original atualizado: {caminho_csv_original}")


# ▶️ EXECUÇÃO
if __name__ == "__main__":
    atualizar_csv_original(
        r"src\Tratamento de CSV e JSON\questoes_pc2025.csv",
        r"src\gabaritos\pc2025_gabarito.csv"
    )
