import json
from collections import defaultdict

def verificar_duplicatas_dataset(caminho_json):
    """
    Verifica se há questões duplicadas no dataset JSON
    """
    with open(caminho_json, encoding="utf-8-sig") as f:
        dados = json.load(f)
    
    # Dicionários para rastrear duplicatas
    ids_dict = defaultdict(list)
    enunciados_dict = defaultdict(list)
    duplicatas_id = []
    duplicatas_enunciado = []
    
    print(f"Analisando {caminho_json}...")
    print(f"Total de questões: {len(dados)}\n")
    
    # Procura por IDs duplicados
    for idx, questao in enumerate(dados):
        id_q = questao.get("id", "")
        enunciado = questao.get("enunciado", "")
        
        ids_dict[id_q].append(idx)
        enunciados_dict[enunciado].append(idx)
    
    # Identifica IDs duplicados
    for id_q, indices in ids_dict.items():
        if len(indices) > 1:
            duplicatas_id.append((id_q, indices))
    
    # Identifica enunciados duplicados (mesma questão com respostas diferentes)
    for enunciado, indices in enunciados_dict.items():
        if len(indices) > 1:
            duplicatas_enunciado.append((enunciado[:80] + "..." if len(enunciado) > 80 else enunciado, indices))
    
    # Relatório
    print("===== RELATÓRIO DE DUPLICATAS =====\n")
    
    if duplicatas_id:
        print(f"⚠️  IDs DUPLICADOS: {len(duplicatas_id)}\n")
        for id_q, indices in duplicatas_id:
            print(f"ID: {id_q}")
            print(f"  Aparições: {len(indices)}")
            print(f"  Índices: {indices}")
            # Mostrar alternativas diferentes
            alternativas_diferentes = set()
            for idx in indices:
                alt = dados[idx].get("alternativas", {})
                alternativas_diferentes.add(json.dumps(alt, sort_keys=True, ensure_ascii=False))
            if len(alternativas_diferentes) > 1:
                print(f"  ⚠️  Alternativas DIFERENTES encontradas!")
            print()
    else:
        print("✅ Nenhum ID duplicado encontrado\n")
    
    if duplicatas_enunciado:
        print(f"⚠️  ENUNCIADOS DUPLICADOS: {len(duplicatas_enunciado)}\n")
        for enunciado, indices in duplicatas_enunciado[:10]:  # Mostra apenas as 10 primeiras
            print(f"Enunciado: {enunciado}")
            print(f"  Aparições: {len(indices)}")
            print(f"  Índices: {indices}")
            # Mostrar respostas corretas diferentes
            if 'label' in dados[0]:  # Se é dataset_label.json
                labels_diferentes = set()
                for idx in indices:
                    label = dados[idx].get("label", "")
                    labels_diferentes.add(label)
                if len(labels_diferentes) > 1:
                    print(f"  ⚠️  Labels DIFERENTES: {labels_diferentes}")
            print()
        
        if len(duplicatas_enunciado) > 10:
            print(f"... e mais {len(duplicatas_enunciado) - 10} enunciados duplicados\n")
    else:
        print("✅ Nenhum enunciado duplicado encontrado\n")
    
    # Resumo
    print("===== RESUMO =====")
    print(f"Total de questões analisadas: {len(dados)}")
    print(f"IDs únicos: {len(ids_dict)}")
    print(f"IDs duplicados: {len(duplicatas_id)}")
    print(f"Enunciados duplicados: {len(duplicatas_enunciado)}")
    
    if duplicatas_id or duplicatas_enunciado:
        print("\n⚠️  Duplicatas encontradas! Revisão necessária.")
    else:
        print("\n✅ Sem duplicatas! Dataset está limpo.")
    
    return len(duplicatas_id) > 0 or len(duplicatas_enunciado) > 0


def comparar_datasets(caminho_dataset, caminho_dataset_label):
    """
    Compara os dois datasets para garantir que têm as mesmas questões
    """
    print("\n\n===== COMPARAÇÃO ENTRE DATASETS =====\n")
    
    with open(caminho_dataset, encoding="utf-8-sig") as f:
        dataset = json.load(f)
    
    with open(caminho_dataset_label, encoding="utf-8-sig") as f:
        dataset_label = json.load(f)
    
    print(f"dataset.json: {len(dataset)} questões")
    print(f"dataset_label.json: {len(dataset_label)} questões")
    
    # Extrai IDs
    ids_dataset = set(q["id"] for q in dataset)
    ids_dataset_label = set(q["id"] for q in dataset_label)
    
    ids_apenas_dataset = ids_dataset - ids_dataset_label
    ids_apenas_label = ids_dataset_label - ids_dataset
    
    if ids_apenas_dataset:
        print(f"\n⚠️  IDs apenas em dataset.json: {len(ids_apenas_dataset)}")
        for id_q in list(ids_apenas_dataset)[:5]:
            print(f"  - {id_q}")
        if len(ids_apenas_dataset) > 5:
            print(f"  ... e mais {len(ids_apenas_dataset) - 5}")
    
    if ids_apenas_label:
        print(f"\n⚠️  IDs apenas em dataset_label.json: {len(ids_apenas_label)}")
        for id_q in list(ids_apenas_label)[:5]:
            print(f"  - {id_q}")
        if len(ids_apenas_label) > 5:
            print(f"  ... e mais {len(ids_apenas_label) - 5}")
    
    if not ids_apenas_dataset and not ids_apenas_label:
        print("\n✅ Ambos os datasets têm as mesmas questões!")
    
    # Verifica se os enunciados são iguais
    enunciados_iguais = 0
    enunciados_diferentes = 0
    
    for q1 in dataset:
        for q2 in dataset_label:
            if q1["id"] == q2["id"]:
                if q1["enunciado"] == q2["enunciado"]:
                    enunciados_iguais += 1
                else:
                    enunciados_diferentes += 1
                break
    
    if enunciados_diferentes == 0:
        print("✅ Todos os enunciados são idênticos entre os datasets!")


# ▶️ EXECUÇÃO
if __name__ == "__main__":
    print("=" * 60)
    print("VERIFICADOR DE DUPLICATAS - DATASET")
    print("=" * 60 + "\n")
    
    # Verifica dataset.json
    tem_duplicatas_dataset = verificar_duplicatas_dataset(
        r"src\Tratamento de CSV e JSON\dataset.json"
    )
    
    # Verifica dataset_label.json
    print("\n" + "=" * 60 + "\n")
    tem_duplicatas_label = verificar_duplicatas_dataset(
        r"src\Tratamento de CSV e JSON\dataset_label.json"
    )
    
    # Compara os datasets
    comparar_datasets(
        r"src\Tratamento de CSV e JSON\dataset.json",
        r"src\Tratamento de CSV e JSON\dataset_label.json"
    )
    
    print("\n" + "=" * 60)
    print("ANÁLISE CONCLUÍDA")
    print("=" * 60)
