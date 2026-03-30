import json
import csv

def validar_questoes(dados):
    erros = []
    ids = set()
    numeros = set()
    questoes_invalidas = set()

    for i, q in enumerate(dados):
        prefixo = f"Questão índice {i}"
        erro_na_questao = False

        # Campos obrigatórios
        campos = ["id", "numero", "enunciado", "alternativas", "correta"]
        for campo in campos:
            if campo not in q:
                erros.append(f"{prefixo}: campo '{campo}' faltando")
                erro_na_questao = True

        # ID duplicado
        if "id" in q:
            if q["id"] in ids:
                erros.append(f"{prefixo}: id duplicado ({q['id']})")
                erro_na_questao = True
            ids.add(q["id"])

        # Número duplicado
        if "numero" in q:
            if q["numero"] in numeros:
                erros.append(f"{prefixo}: número duplicado ({q['numero']})")
                erro_na_questao = True
            numeros.add(q["numero"])

        # Alternativas
        if "alternativas" in q:
            alternativas = q["alternativas"]

            if not isinstance(alternativas, dict):
                erros.append(f"{prefixo}: alternativas não é um dicionário")
                erro_na_questao = True
            else:
                letras_esperadas = {"A", "B", "C", "D", "E"}

                faltando = letras_esperadas - set(alternativas.keys())
                extras = set(alternativas.keys()) - letras_esperadas

                if faltando:
                    erros.append(f"{prefixo}: faltando alternativas {faltando}")
                    erro_na_questao = True
                if extras:
                    erros.append(f"{prefixo}: alternativas inválidas {extras}")
                    erro_na_questao = True

        # Correta
        if "correta" in q and "alternativas" in q:
            if isinstance(q["alternativas"], dict):
                if q["correta"] not in q["alternativas"]:
                    erros.append(f"{prefixo}: correta '{q['correta']}' não existe nas alternativas")
                    erro_na_questao = True

        if erro_na_questao:
            questoes_invalidas.add(i)

    return erros, questoes_invalidas


def json_para_csv(caminho_json, caminho_csv, caminho_log="erros.txt"):
    with open(caminho_json, "r", encoding="utf-8") as f:
        dados = json.load(f)

    erros, invalidas = validar_questoes(dados)

    total = len(dados)
    total_invalidas = len(invalidas)
    total_validas = total - total_invalidas

    # Salvar log de erros
    if erros:
        with open(caminho_log, "w", encoding="utf-8") as log:
            log.write("RELATÓRIO DE ERROS\n")
            log.write("=" * 40 + "\n\n")
            for e in erros:
                log.write(e + "\n")

        print(f"❌ {total_invalidas} questões inválidas encontradas.")
        print(f"📄 Veja o arquivo '{caminho_log}' para detalhes.\n")
    else:
        print("✅ Nenhum erro encontrado!\n")

    print(f"📊 RESUMO:")
    print(f"Total de questões: {total}")
    print(f"Válidas: {total_validas}")
    print(f"Inválidas: {total_invalidas}\n")

    # Só exporta as válidas
    with open(caminho_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "enunciado", "alternativa", "texto_alt", "label"])

        for i, q in enumerate(dados):
            if i in invalidas:
                continue  # pula inválidas

            for letra, texto in q["alternativas"].items():
                label = 1 if letra == q["correta"] else 0

                writer.writerow([
                    q["id"],
                    q["enunciado"],
                    letra,
                    texto,
                    label
                ])

    print("✅ CSV gerado apenas com questões válidas!")


# USO
json_para_csv("src/dataset/dataset_label.json", "src/txt/todasasquestoes.csv")