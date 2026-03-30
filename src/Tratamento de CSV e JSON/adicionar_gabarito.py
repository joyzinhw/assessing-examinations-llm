import csv
import json
import re

def extrair_numero_questao(id_questao):
    """Extrai o número da questão do ID (último número após underscore)"""
    match = re.search(r'_(\d+)$', id_questao)
    return int(match.group(1)) if match else None


def carregar_gabarito(caminho_gabarito):
    """Carrega o gabarito em um dicionário com chave ID completo"""
    gabarito_dict = {}
    
    with open(caminho_gabarito, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter=",")
        for linha in reader:
            id_q = linha["id"].strip()
            resposta = linha["resposta"].strip()
            gabarito_dict[id_q] = resposta
    
    print(f"✓ Gabarito carregado: {len(gabarito_dict)} entradas")
    return gabarito_dict


def carregar_dataset_json(caminho_json):
    """Carrega o dataset JSON"""
    with open(caminho_json, encoding="utf-8") as f:
        return json.load(f)


def adicionar_gabarito_ao_json(dataset, gabarito):
    """Adiciona o campo 'resposta' ao dataset usando o gabarito"""
    questoes_com_resposta = 0
    questoes_sem_resposta = []
    
    for questao in dataset:
        id_q = questao.get("id", "").strip()
        numero_q = questao.get("numero")
        
        # Extrai prova do ID (ex: "01" de "pc2025_01_pn_32")
        partes = id_q.split("_")
        if len(partes) >= 2:
            prova = partes[1]  # Ex: "01"
            
            # Monta o ID que deve estar no gabarito (ex: "pc2025_01_32")
            id_gabarito = f"pc2025_{prova}_{numero_q}"
            
            if id_gabarito in gabarito:
                questao["resposta"] = gabarito[id_gabarito]
                questoes_com_resposta += 1
            else:
                questoes_sem_resposta.append(id_q + f" (procurou por {id_gabarito})")
        else:
            questoes_sem_resposta.append(id_q + " (ID inválido)")
    
    return dataset, questoes_com_resposta, questoes_sem_resposta


def salvar_dataset_com_gabarito(dataset, caminho_saida):
    """Salva o dataset enriquecido em formato JSON"""
    with open(caminho_saida, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)
    
    print(f"✓ Dataset com gabarito salvo em: {caminho_saida}")


def processar_pc2025():
    """Processa o PC2025: carrega dataset, enriquece com gabarito e salva"""
    # Caminhos
    caminho_dataset = "dataset.json"
    caminho_gabarito = "../gabaritos/pc2025_gabarito.csv"
    caminho_saida = "dataset_label.json"
    
    print("\n==== PROCESSANDO PC2025 ====")
    print(f"Carregando dataset de: {caminho_dataset}")
    dataset = carregar_dataset_json(caminho_dataset)
    print(f"✓ Dataset carregado: {len(dataset)} questões")
    
    print(f"\nCarregando gabarito de: {caminho_gabarito}")
    gabarito = carregar_gabarito(caminho_gabarito)
    
    print(f"\nAdicionando respostas corretas ao dataset...")
    dataset_com_gabarito, com_resposta, sem_resposta = adicionar_gabarito_ao_json(dataset, gabarito)
    
    print(f"✓ Questões enriquecidas: {com_resposta}")
    if sem_resposta:
        print(f"⚠ Questões sem gabarito: {len(sem_resposta)}")
        for id_q in sem_resposta[:5]:
            print(f"  - {id_q}")
    
    print(f"\nSalvando arquivo final...")
    salvar_dataset_com_gabarito(dataset_com_gabarito, caminho_saida)
    print(f"\n✓ Processo concluído com sucesso!")


if __name__ == "__main__":
    processar_pc2025()
