import csv
import json
import re
from collections import defaultdict


def extrair_numero(id_questao):
    match = re.search(r'_(\d+)$', id_questao)
    return int(match.group(1)) if match else None


def detectar_delimitador(caminho_csv):
    """
    Detecta automaticamente se o CSV usa , ou ;
    """
    with open(caminho_csv, encoding="utf-8-sig") as f:
        primeira_linha = f.readline()
        # Contar separadores na primeira linha (cabeçalho) onde não há aspas
        if primeira_linha.count(";") > 0:
            return ";"
        return ","


def validar_linha(linha, linha_num):
    erros = []

    if not linha.get("id"):
        erros.append(f"Linha {linha_num}: ID vazio")

    if not linha.get("enunciado"):
        erros.append(f"Linha {linha_num}: enunciado vazio")

    if linha.get("opcao") not in ["A", "B", "C", "D", "E"]:
        erros.append(f"Linha {linha_num}: opção inválida ({linha.get('opcao')})")

    # Aceita 0/1 (formato antigo) ou A-E (gabarito do formato novo)
    resposta = linha.get("resposta", "").strip()
    if resposta not in ["0", "1", "A", "B", "C", "D", "E"]:
        erros.append(f"Linha {linha_num}: resposta inválida ({resposta})")

    return erros


def detectar_delimitador(caminho_csv):
    """
    Detecta automaticamente se o CSV usa , ou ;
    """
    with open(caminho_csv, encoding="utf-8-sig") as f:
        primeira_linha = f.readline()
        # Contar separadores na primeira linha (cabeçalho) onde não há aspas
        if primeira_linha.count(";") > 0:
            return ";"
        return ","


def csv_para_json(caminho_csv, caminho_dataset, caminho_dataset_label, debug=False):
    questoes = defaultdict(lambda: {
        "id": "",
        "numero": None,
        "enunciado": "",
        "alternativas": {},
        "correta": None
    })

    erros = []
    total_linhas = 0

    delimitador = detectar_delimitador(caminho_csv)

    print(f"Delimitador detectado: '{delimitador}'")
    print("Processando CSV...")

    with open(caminho_csv, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter=delimitador)

        for i, linha in enumerate(reader, start=2):
            total_linhas += 1

            # Validação
            erros_linha = validar_linha(linha, i)
            if erros_linha:
                erros.extend(erros_linha)
                continue

            id_q = linha["id"].strip()
            enunciado = linha["enunciado"].strip()
            opcao = linha["opcao"].strip()
            texto = linha["texto_alternativa"].strip()
            resposta = linha["resposta"].strip()

            q = questoes[id_q]

            q["id"] = id_q
            q["numero"] = extrair_numero(id_q)
            q["enunciado"] = enunciado
            q["alternativas"][opcao] = texto

            # Compatível com ambos os formatos:
            # - Formato antigo: resposta é "1" se é correta, "0" se não é
            # - Formato novo (gabarito): resposta é a letra da alternativa correta (A, B, C, D, E)
            if resposta in ["A", "B", "C", "D", "E"]:
                # Novo formato: resposta é a letra
                if resposta == opcao:
                    if q["correta"] is not None:
                        erros.append(f"Questão {id_q}: mais de uma alternativa correta")
                    q["correta"] = opcao
            elif resposta == "1":
                # Formato antigo: resposta é "1"
                if q["correta"] is not None:
                    erros.append(f"Questão {id_q}: mais de uma alternativa correta")
                q["correta"] = opcao

    # Validação final
    questoes_finais = []
    for id_q, q in questoes.items():
        if len(q["alternativas"]) != 5:
            erros.append(f"Questão {id_q}: possui {len(q['alternativas'])} alternativas (esperado: 5)")

        if q["correta"] is None:
            erros.append(f"Questão {id_q}: sem alternativa correta")

        questoes_finais.append(q)

    # Preparar dados para dataset.json (sem a label)
    dataset = []
    for q in questoes_finais:
        item = {
            "id": q["id"],
            "numero": q["numero"],
            "enunciado": q["enunciado"],
            "alternativas": q["alternativas"]
        }
        dataset.append(item)

    # Preparar dados para dataset_label.json (com a label)
    dataset_label = []
    for q in questoes_finais:
        item = {
            "id": q["id"],
            "numero": q["numero"],
            "enunciado": q["enunciado"],
            "alternativas": q["alternativas"],
            "label": q["correta"]
        }
        dataset_label.append(item)

    # Salvar JSONs
    with open(caminho_dataset, "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)

    with open(caminho_dataset_label, "w", encoding="utf-8") as f:
        json.dump(dataset_label, f, ensure_ascii=False, indent=2)

    # Relatório
    print("\n===== RELATÓRIO =====")
    print(f"Total de linhas lidas: {total_linhas}")
    print(f"Total de questões: {len(questoes_finais)}")
    print(f"Total de erros: {len(erros)}")
    print(f"\nArquivos gerados:")
    print(f"- {caminho_dataset}")
    print(f"- {caminho_dataset_label}")

    if erros:
        print("\nErros encontrados:")
        for e in erros[:20]:  # limita pra não floodar
            print("-", e)
        if len(erros) > 20:
            print(f"... e mais {len(erros) - 20} erros")
    else:
        print("Nenhum erro encontrado ✅")


# ▶️ EXECUÇÃO (IMPORTANTE usar r"" no caminho)
csv_para_json(
    r"src\Tratamento de CSV e JSON\questoes_pc2025_com_gabarito.csv",
    r"src\Tratamento de CSV e JSON\dataset.json",
    r"src\Tratamento de CSV e JSON\dataset_label.json",
    debug=False  # Debug desativado
)