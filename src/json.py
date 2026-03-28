#sem label

import os
import re
import json
from docx import Document

PASTA_TXT = "src/txt"
PASTA_GABARITO = "src/gabaritos"
SAIDA = "src/dataset/dataset.json"

dados = []

todas_questoes = []
questoes_validas = []
questoes_removidas = []

# ======================
# 🔹 LER TXT
# ======================
def ler_txt(caminho):
    with open(caminho, "r", encoding="utf-8") as f:
        return f.read()

# ======================
# 🔹 LER DOCX
# ======================
def ler_docx(caminho):
    doc = Document(caminho)
    return "\n".join([p.text for p in doc.paragraphs])

# ======================
# 🔹 EXTRAIR GABARITO
# ======================
def extrair_gabarito(texto):
    texto = texto.upper()

    padrao = r'(\d{1,3})\s*(A\*|B\*|C\*|D\*|E\*|A|B|C|D|E|NULA|ANULADA)'
    matches = re.findall(padrao, texto)

    gabarito = {}

    for numero, resposta in matches:
        numero = int(numero)
        resposta = resposta.replace("*", "")

        if resposta in ["NULA", "ANULADA"]:
            gabarito[numero] = "ANULADA"
        else:
            gabarito[numero] = resposta

    return gabarito

# ======================
# 🔹 EXTRAIR QUESTÕES
# ======================
def extrair_questoes(texto):
    partes = re.split(r'(?:^|\n)\s*(\d{1,3})\.\s', texto)

    questoes = []

    for i in range(1, len(partes), 2):
        numero = int(partes[i])
        conteudo = partes[i + 1]
        questoes.append((numero, conteudo.strip()))

    return questoes

# ======================
# 🔹 EXTRAIR ALTERNATIVAS
# ======================
def extrair_alternativas(texto):
    # pega todas as alternativas
    padrao = r'([a-e])\)\s*(.*?)(?=\n[a-e]\)|$)'

    matches = re.findall(padrao, texto, re.DOTALL | re.IGNORECASE)

    alternativas = {}

    for letra, conteudo in matches:
        alternativas[letra.upper()] = conteudo.strip()

    if not alternativas:
        return texto.strip(), {}

    # 🔥 remove TODAS as alternativas do texto
    texto_sem_alternativas = re.sub(
        r'\n?\s*[a-e]\)\s*.*?(?=\n[a-e]\)|$)',
        '',
        texto,
        flags=re.IGNORECASE | re.DOTALL
    )

    # 🔥 remove qualquer resquício tipo "a)" no meio do enunciado
    texto_sem_alternativas = re.sub(r'\b[a-e]\)\s*', '', texto_sem_alternativas, flags=re.IGNORECASE)

    enunciado = texto_sem_alternativas.strip()

    return enunciado, alternativas


# ======================
# 🔹 EXTRAIR ITENS
# ======================
def extrair_itens(texto):
    padrao = r'\b(I{1,3}V?)\.\s*(.*?)\s*(?=(I{1,3}V?\.)|$)'
    itens = re.findall(padrao, texto, re.DOTALL)

    return [{"item": i[0], "texto": i[1].strip()} for i in itens]

# ======================
# 🔹 CARREGAR GABARITOS
# ======================
gabaritos = {}

for arquivo in os.listdir(PASTA_GABARITO):
    if not arquivo.endswith(".docx"):
        continue

    print(f"\n📥 Lendo gabarito: {arquivo}")

    caminho = os.path.join(PASTA_GABARITO, arquivo)
    texto = ler_docx(caminho)

    nome_prova = arquivo.split("_")[0]
    gabaritos[nome_prova] = extrair_gabarito(texto)

# ======================
# 🔹 PROCESSAR QUESTÕES
# ======================
for arquivo in os.listdir(PASTA_TXT):
    if not arquivo.endswith(".txt"):
        continue

    print(f"\n📄 Processando: {arquivo}")

    caminho = os.path.join(PASTA_TXT, arquivo)
    texto = ler_txt(caminho)
    questoes = extrair_questoes(texto)

    nome_prova = arquivo.split("_")[0]
    tipo = arquivo.split("_")[1].replace(".txt", "").lower()

    gabarito_prova = gabaritos.get(nome_prova, {})

    if nome_prova == "pm2021":
        inicio, fim = 21, 54
    elif nome_prova == "pp2024":
        inicio, fim = 21, 52
    else:
        inicio, fim = 1, 999

    encontradas = set()

    for numero, conteudo in questoes:

        todas_questoes.append((nome_prova, tipo, numero))
        encontradas.add(numero)

        if numero < inicio or numero > fim:
            print(f"🚫 FORA DO INTERVALO -> {nome_prova}_{tipo} | Q{numero}")
            continue

        if numero not in gabarito_prova:
            print(f"❌ REMOVIDA (sem gabarito) -> {nome_prova}_{tipo} | Q{numero}")
            questoes_removidas.append((nome_prova, tipo, numero))
            continue

        # 🔥 tratar anuladas explicitamente
        if gabarito_prova[numero] == "ANULADA":
            print(f"⚠️ ANULADA -> {nome_prova}_{tipo} | Q{numero}")
            continue

        enunciado, alternativas = extrair_alternativas(conteudo)

        if len(alternativas) == 0:
            print(f"⚠️ SEM ALTERNATIVAS -> {nome_prova}_{tipo} | Q{numero}")
            continue

        print(f"✅ OK -> {nome_prova}_{tipo} | Q{numero}")

        questoes_validas.append((nome_prova, tipo, numero))

        item = {
            "id": f"{nome_prova}_{tipo}_{numero}",
            "numero": numero,
            "enunciado": enunciado,
            "alternativas": alternativas
        }

        itens = extrair_itens(enunciado)
        if itens:
            item["itens"] = itens

        dados.append(item)

    esperadas = set(range(inicio, fim + 1))
    faltando = esperadas - encontradas

    if faltando:
        print(f"⚠️ FALTANDO -> {nome_prova}_{tipo}: {sorted(faltando)}")
    else:
        print(f"✅ COMPLETA -> {nome_prova}_{tipo}")

# ======================
# 🔹 SALVAR JSON
# ======================
with open(SAIDA, "w", encoding="utf-8") as f:
    json.dump(dados, f, ensure_ascii=False, indent=2)

# ======================
# 🔹 RESUMO FINAL
# ======================
print("\n==============================")
print("📊 RESUMO FINAL")
print("==============================")

print(f"📝 Total encontradas: {len(todas_questoes)}")
print(f"✅ Válidas: {len(questoes_validas)}")
print(f"❌ Removidas: {len(set(questoes_removidas))}")

print("\n🎯 CHECK FINAL")
print("Esperado: 198")
print("Obtido:", len(dados))

# com label

import os
import re
import json
from docx import Document

PASTA_TXT = "src/txt"
PASTA_GABARITO = "src/gabaritos"
SAIDA = "src/dataset/dataset_label.json"

dados = []

todas_questoes = []
questoes_validas = []
questoes_removidas = []

# ======================
# 🔹 LER TXT
# ======================
def ler_txt(caminho):
    with open(caminho, "r", encoding="utf-8") as f:
        return f.read()

# ======================
# 🔹 LER DOCX
# ======================
def ler_docx(caminho):
    doc = Document(caminho)
    return "\n".join([p.text for p in doc.paragraphs])

# ======================
# 🔹 EXTRAIR GABARITO
# ======================
def extrair_gabarito(texto):
    texto = texto.upper()

    padrao = r'(\d{1,3})\s*(A\*|B\*|C\*|D\*|E\*|A|B|C|D|E|NULA|ANULADA)'
    matches = re.findall(padrao, texto)

    gabarito = {}

    for numero, resposta in matches:
        numero = int(numero)
        resposta = resposta.replace("*", "")

        if resposta in ["NULA", "ANULADA"]:
            gabarito[numero] = "ANULADA"
        else:
            gabarito[numero] = resposta

    return gabarito
# ======================
# 🔹 EXTRAIR QUESTÕES (CORRIGIDO)
# ======================
def extrair_questoes(texto):
    # 🔥 FIX: agora pega a questão 21 também
    partes = re.split(r'(?:^|\n)\s*(\d{1,3})\.\s', texto)

    questoes = []

    for i in range(1, len(partes), 2):
        numero = int(partes[i])
        conteudo = partes[i + 1]
        questoes.append((numero, conteudo.strip()))

    return questoes

# ======================
# 🔹 EXTRAIR ALTERNATIVAS (CORRIGIDO)
# ======================
def extrair_alternativas(texto):
    # pega todas as alternativas
    padrao = r'([a-e])\)\s*(.*?)(?=\n[a-e]\)|$)'

    matches = re.findall(padrao, texto, re.DOTALL | re.IGNORECASE)

    alternativas = {}

    for letra, conteudo in matches:
        alternativas[letra.upper()] = conteudo.strip()

    if not alternativas:
        return texto.strip(), {}

    # 🔥 remove TODAS as alternativas do texto
    texto_sem_alternativas = re.sub(
        r'\n?\s*[a-e]\)\s*.*?(?=\n[a-e]\)|$)',
        '',
        texto,
        flags=re.IGNORECASE | re.DOTALL
    )

    # 🔥 remove qualquer resquício tipo "a)" no meio do enunciado
    texto_sem_alternativas = re.sub(r'\b[a-e]\)\s*', '', texto_sem_alternativas, flags=re.IGNORECASE)

    enunciado = texto_sem_alternativas.strip()

    return enunciado, alternativas

# ======================
# 🔹 EXTRAIR ITENS
# ======================
def extrair_itens(texto):
    padrao = r'\b(I{1,3}V?)\.\s*(.*?)\s*(?=(I{1,3}V?\.)|$)'
    itens = re.findall(padrao, texto, re.DOTALL)

    return [{"item": i[0], "texto": i[1].strip()} for i in itens]

# ======================
# 🔹 CARREGAR GABARITOS
# ======================
gabaritos = {}

for arquivo in os.listdir(PASTA_GABARITO):
    if not arquivo.endswith(".docx"):
        continue

    print(f"\n📥 Lendo gabarito: {arquivo}")

    caminho = os.path.join(PASTA_GABARITO, arquivo)
    texto = ler_docx(caminho)

    nome_prova = arquivo.split("_")[0]
    gabaritos[nome_prova] = extrair_gabarito(texto)

# ======================
# 🔹 PROCESSAR QUESTÕES
# ======================
for arquivo in os.listdir(PASTA_TXT):
    if not arquivo.endswith(".txt"):
        continue

    print(f"\n📄 Processando: {arquivo}")

    caminho = os.path.join(PASTA_TXT, arquivo)
    texto = ler_txt(caminho)
    questoes = extrair_questoes(texto)

    nome_prova = arquivo.split("_")[0]
    tipo = arquivo.split("_")[1].replace(".txt", "").lower()

    gabarito_prova = gabaritos.get(nome_prova, {})

    if nome_prova == "pm2021":
        inicio, fim = 21, 54
    elif nome_prova == "pp2024":
        inicio, fim = 21, 52
    else:
        inicio, fim = 1, 999

    encontradas = set()

    for numero, conteudo in questoes:

        todas_questoes.append((nome_prova, tipo, numero))
        encontradas.add(numero)

        # fora do intervalo
        if numero < inicio or numero > fim:
            print(f"🚫 FORA DO INTERVALO -> {nome_prova}_{tipo} | Q{numero}")
            continue

        # sem gabarito (anulada)
        if numero not in gabarito_prova:
            print(f"❌ REMOVIDA (sem gabarito) -> {nome_prova}_{tipo} | Q{numero}")
            questoes_removidas.append((nome_prova, tipo, numero))
            continue

        # 🔥 tratar anuladas explicitamente
        if gabarito_prova[numero] == "ANULADA":
            print(f"⚠️ ANULADA -> {nome_prova}_{tipo} | Q{numero}")
            continue

        enunciado, alternativas = extrair_alternativas(conteudo)

        # 🔥 AGORA Q53 NÃO É MAIS DESCARTADA INJUSTAMENTE
        if len(alternativas) == 0:
            print(f"⚠️ SEM ALTERNATIVAS -> {nome_prova}_{tipo} | Q{numero}")
            continue

        resposta = gabarito_prova[numero]

        print(f"✅ OK -> {nome_prova}_{tipo} | Q{numero} | {resposta}")

        questoes_validas.append((nome_prova, tipo, numero))

        item = {
            "id": f"{nome_prova}_{tipo}_{numero}",
            "numero": numero,
            "enunciado": enunciado,
            "alternativas": alternativas,
            "correta": resposta
        }

        itens = extrair_itens(enunciado)
        if itens:
            item["itens"] = itens

        dados.append(item)

    esperadas = set(range(inicio, fim + 1))
    faltando = esperadas - encontradas

    if faltando:
        print(f"⚠️ FALTANDO -> {nome_prova}_{tipo}: {sorted(faltando)}")
    else:
        print(f"✅ COMPLETA -> {nome_prova}_{tipo}")

# ======================
# 🔹 SALVAR JSON
# ======================
with open(SAIDA, "w", encoding="utf-8") as f:
    json.dump(dados, f, ensure_ascii=False, indent=2)


print("\n==============================")
print("📊 RESUMO FINAL")
print("==============================")

print(f"📝 Total encontradas: {len(todas_questoes)}")
print(f"✅ Válidas: {len(questoes_validas)}")
print(f"❌ Removidas: {len(set(questoes_removidas))}")

print("\n🎯 CHECK FINAL")
print("Esperado: 198")
print("Obtido:", len(dados))