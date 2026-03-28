

# #transforma cvs em json todo organizado
# import csv
# import json

# dados = {}

# with open("src/dataset/cvs-test.csv", encoding="utf-8") as f:
#     reader = csv.reader(f, delimiter=",", quotechar='"')

#     next(reader)  

#     for row in reader:
#         if len(row) < 5:
#             continue

#         id_, enunciado, alternativa, texto_alt, label = row[:5]

#         try:
#             label = int(label)
#         except:
#             continue

#         if id_ not in dados:
#             dados[id_] = {
#                 "id": id_,
#                 "pergunta": enunciado,
#                 "alternativas": {},
#                 "correta": None
#             }

#         dados[id_]["alternativas"][alternativa] = texto_alt

#         if label == 1:
#             dados[id_]["correta"] = alternativa

# resultado = [v for v in dados.values() if v["correta"]]

# with open("src/dataset/dataset.json", "w", encoding="utf-8") as f:
#     json.dump(resultado, f, ensure_ascii=False, indent=2)

# print("Total de questões:", len(resultado))

import os
import re
import json
from docx import Document

PASTA = "src/concursos/pp2024/Provas"
SAIDA = "src/dataset/pp2024.json"

dados = []

# ======================
# 🔹 FUNÇÃO: LER DOCX
# ======================
def ler_docx(caminho):
    doc = Document(caminho)
    texto = []
    for p in doc.paragraphs:
        if p.text.strip():
            texto.append(p.text.strip())
    return "\n".join(texto)


# ======================
# 🔹 QUEBRAR QUESTÕES (ROBUSTO)
# ======================
def extrair_questoes(texto):
    # aceita: 21. 21) 21 - 21
    padrao = r'\n?\s*(\d{1,3})[\.\)\-]?\s+'
    partes = re.split(padrao, texto)

    questoes = []

    for i in range(1, len(partes), 2):
        try:
            numero = int(partes[i])
            conteudo = partes[i+1]
            questoes.append((numero, conteudo.strip()))
        except:
            continue

    return questoes


# ======================
# 🔹 EXTRAI ALTERNATIVAS (ROBUSTO)
# ======================
def extrair_alternativas(texto):
    # aceita: a) A) (a) A. a - etc + inclui E
    padrao = r'[\(\[]?([A-Ea-e])[\)\]\.\-]\s*'
    partes = re.split(padrao, texto)

    if len(partes) < 3:
        return texto.strip(), {}

    enunciado = partes[0].strip()
    alternativas = {}

    for i in range(1, len(partes), 2):
        letra = partes[i].upper()
        conteudo = partes[i+1].strip()
        alternativas[letra] = conteudo

    return enunciado, alternativas


# ======================
# 🔹 PROCESSAR ARQUIVOS
# ======================
for arquivo in os.listdir(PASTA):
    if not arquivo.endswith(".docx"):
        continue

    caminho = os.path.join(PASTA, arquivo)

    print(f"Processando: {arquivo}")

    texto = ler_docx(caminho)
    questoes = extrair_questoes(texto)

    print(f"  -> {len(questoes)} questões encontradas")

    # identifica tipo: a, b, c
    tipo = arquivo.split("_")[-1].replace(".docx", "").lower()

    for numero, conteudo in questoes:
        if numero < 21 or numero > 52:
            continue

        enunciado, alternativas = extrair_alternativas(conteudo)

        # 🔥 NÃO descarta tão fácil
        if len(alternativas) < 3:
            continue

        item = {
            "id": f"pp2024_{tipo}_{numero}",
            "pergunta": enunciado,
            "alternativas": alternativas,
            "correta": None
        }

        dados.append(item)


# ======================
# 🔹 SALVAR JSON
# ======================
with open(SAIDA, "w", encoding="utf-8") as f:
    json.dump(dados, f, ensure_ascii=False, indent=2)

print("✅ Total de questões:", len(dados))