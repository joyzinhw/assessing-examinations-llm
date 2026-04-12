# import json
# import re

# INPUT_PATH = "src/dataset/dataset.json"
# OUTPUT_PATH = "src/dataset/dataset_tratado.json"

# # regex mais robusto
# PADRAO_ITENS = re.compile(r"(I{1,3}|IV|V|VI|VII|VIII|IX|X)\.\s")

# # frases que indicam fim dos itens
# FIM_PADROES = [
#     "Está correto",
#     "Assinale",
#     "Está(ão) correto",
#     "É correto afirmar",
# ]

# def limpar_final(texto):
#     for padrao in FIM_PADROES:
#         idx = texto.find(padrao)
#         if idx != -1:
#             return texto[:idx].strip(), texto[idx:].strip()
#     return texto, ""

# def extrair_itens(enunciado):
#     matches = list(PADRAO_ITENS.finditer(enunciado))

#     if len(matches) < 2:
#         return enunciado, None

#     itens = []

#     for i, match in enumerate(matches):
#         inicio = match.end()

#         if i + 1 < len(matches):
#             fim = matches[i + 1].start()
#         else:
#             fim = len(enunciado)

#         numero = match.group(1)
#         texto = enunciado[inicio:fim].strip()

#         # 🔥 limpa final do último item
#         if i == len(matches) - 1:
#             texto, resto = limpar_final(texto)
#         else:
#             resto = ""

#         itens.append({
#             "item": numero,
#             "texto": texto
#         })

#     # 🔥 enunciado limpo = antes do primeiro item + resto final
#     inicio_itens = matches[0].start()
#     enunciado_base = enunciado[:inicio_itens].strip()

#     # pega final (ex: "Está correto...")
#     _, final = limpar_final(enunciado)

#     enunciado_final = (enunciado_base + " " + final).strip()

#     return enunciado_final, itens


# # ======================
# # 🔹 PROCESSAR
# # ======================
# with open(INPUT_PATH, "r", encoding="utf-8") as f:
#     dataset = json.load(f)

# novo_dataset = []

# for q in dataset:
#     if not isinstance(q, dict):
#         continue

#     enunciado = q.get("enunciado", "")

#     enunciado_limpo, itens = extrair_itens(enunciado)

#     if itens:
#         q["enunciado"] = enunciado_limpo
#         q["itens"] = itens

#     novo_dataset.append(q)

# # ======================
# # 🔹 SALVAR
# # ======================
# with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
#     json.dump(novo_dataset, f, ensure_ascii=False, indent=2)

# print("✅ Dataset tratado com sucesso!")


import json
import re

INPUT_PATH = "src/dataset/dataset.json"
OUTPUT_PATH = "src/dataset/dataset_tratado.json"

# ======================
# 🔹 PADRÕES
# ======================

# itens romanos
PADRAO_ITENS = re.compile(r"(I{1,3}|IV|V|VI|VII|VIII|IX|X)\.\s")

# itens V/F → ( ) texto
PADRAO_VF = re.compile(r"\(\s*\)\s*(.*?)(?=\(\s*\)|$)", re.DOTALL)

# frases que indicam fim dos itens
FIM_PADROES = [
    "Está correto",
    "Assinale",
    "Está(ão) correto",
    "É correto afirmar",
    "A sequência correta",
]

# ======================
# 🔹 LIMPAR FINAL
# ======================
def limpar_final(texto):
    for padrao in FIM_PADROES:
        idx = texto.find(padrao)
        if idx != -1:
            return texto[:idx].strip(), texto[idx:].strip()
    return texto, ""

# ======================
# 🔹 EXTRAIR ITENS V/F
# ======================
def extrair_itens_vf(enunciado):
    matches = PADRAO_VF.findall(enunciado)

    if len(matches) < 2:
        return None, None

    itens = []

    for i, texto in enumerate(matches):
        texto_limpo, _ = limpar_final(texto)

        itens.append({
            "item": str(i + 1),
            "texto": texto_limpo.strip()
        })

    # remove os itens do enunciado
    enunciado_sem_itens = PADRAO_VF.sub("", enunciado).strip()

    # recupera final (ex: "A sequência correta...")
    _, final = limpar_final(enunciado)

    enunciado_final = (enunciado_sem_itens + " " + final).strip()

    return enunciado_final, itens

# ======================
# 🔹 EXTRAIR ITENS ROMANOS
# ======================
def extrair_itens_romanos(enunciado):
    matches = list(PADRAO_ITENS.finditer(enunciado))

    if len(matches) < 2:
        return None, None

    itens = []

    for i, match in enumerate(matches):
        inicio = match.end()

        if i + 1 < len(matches):
            fim = matches[i + 1].start()
        else:
            fim = len(enunciado)

        numero = match.group(1)
        texto = enunciado[inicio:fim].strip()

        # limpa final do último item
        if i == len(matches) - 1:
            texto, _ = limpar_final(texto)

        itens.append({
            "item": numero,
            "texto": texto
        })

    # enunciado base
    inicio_itens = matches[0].start()
    enunciado_base = enunciado[:inicio_itens].strip()

    _, final = limpar_final(enunciado)

    enunciado_final = (enunciado_base + " " + final).strip()

    return enunciado_final, itens

# ======================
# 🔹 PROCESSAR QUESTÃO
# ======================
def processar_questao(q):
    enunciado = q.get("enunciado", "")

    # 🔥 1. tenta V/F primeiro
    enunciado_vf, itens_vf = extrair_itens_vf(enunciado)

    if itens_vf:
        q["enunciado"] = enunciado_vf
        q["itens"] = itens_vf
        q["tipo"] = "VF"
        return q

    # 🔥 2. tenta romanos
    enunciado_itens, itens = extrair_itens_romanos(enunciado)

    if itens:
        q["enunciado"] = enunciado_itens
        q["itens"] = itens
        q["tipo"] = "MULTIPLOS_ITENS"
        return q

    return q

# ======================
# 🔹 PROCESSAR DATASET
# ======================
with open(INPUT_PATH, "r", encoding="utf-8") as f:
    dataset = json.load(f)

novo_dataset = []

for q in dataset:
    if not isinstance(q, dict):
        continue

    q = processar_questao(q)
    novo_dataset.append(q)

# ======================
# 🔹 SALVAR
# ======================
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(novo_dataset, f, ensure_ascii=False, indent=2)

print("✅ Dataset tratado com sucesso!")