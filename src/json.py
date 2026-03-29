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

def ler_txt(caminho):
    with open(caminho, "r", encoding="utf-8") as f:
        return f.read()

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
def extrair_questoes(texto):
    partes = re.split(r'(?:^|\n)\s*(\d{1,3})\.\s', texto)

    questoes = []

    for i in range(1, len(partes), 2):
        numero = int(partes[i])
        conteudo = partes[i + 1]
        questoes.append((numero, conteudo.strip()))

    return questoes

def extrair_alternativas(texto):
    padrao = r'^\s*([a-e])\)\s*(.*?)(?=^\s*[a-e]\)|$)'

    matches = re.findall(padrao, texto, re.DOTALL | re.IGNORECASE | re.MULTILINE)

    alternativas = {}

    for letra, conteudo in matches:
        alternativas[letra.upper()] = conteudo.strip()

    if not alternativas:
        return texto.strip(), {}

    texto_sem_alternativas = re.sub(
        r'^\s*[a-e]\)\s*.*?(?=^\s*[a-e]\)|$)',
        '',
        texto,
        flags=re.IGNORECASE | re.DOTALL | re.MULTILINE
    )

    enunciado = texto_sem_alternativas.strip()

    return enunciado, alternativas

def extrair_itens(texto):
    padrao = r'(I|II|III|IV)\.\s*(.*?)(?=\n\s*(I|II|III|IV)\.|$)'
    matches = re.findall(padrao, texto, re.DOTALL)

    return [
        {"item": m[0], "texto": m[1].strip()}
        for m in matches
    ]

for arquivo in os.listdir(PASTA_TXT):
    if not arquivo.endswith(".txt"):
        continue

    print(f"\n📄 Processando: {arquivo}")

    caminho = os.path.join(PASTA_TXT, arquivo)
    texto = ler_txt(caminho)
    questoes = extrair_questoes(texto)

    nome_prova = arquivo.split("_")[0]
    tipo = arquivo.split("_")[1].replace(".txt", "").lower()

    

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

enunciados_vistos = {}
dados_unicos = []
duplicadas = []

def normalizar_texto(t):
    t = t.lower().strip()
    t = re.sub(r'\s+', ' ', t)
    return t

for item in dados:
    enunciado_norm = normalizar_texto(item["enunciado"])

    if enunciado_norm in enunciados_vistos:
        duplicadas.append({
            "removida": item["id"],
            "mantida": enunciados_vistos[enunciado_norm]["id"],
            "enunciado": item["enunciado"][:120]  # preview
        })
    else:
        enunciados_vistos[enunciado_norm] = item
        dados_unicos.append(item)

dados = dados_unicos


print("\n🔁 DUPLICADAS REMOVIDAS:", len(duplicadas))

for d in duplicadas:
    print("\n------------------------")
    print(f"❌ Removida: {d['removida']}")
    print(f"✅ Mantida:  {d['mantida']}")
    print(f"📝 Enunciado: {d['enunciado']}...")

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

# com label

PASTA_TXT = "src/txt"
PASTA_GABARITO = "src/gabaritos"
SAIDA = "src/dataset/dataset_label.json"

dados = []

todas_questoes = []
questoes_validas = []
questoes_removidas = []

def ler_txt(caminho):
    with open(caminho, "r", encoding="utf-8") as f:
        return f.read()

def limpar_texto(texto):
    
    texto = re.sub(r'\b(\w+)\s+\1\b', r'\1', texto, flags=re.IGNORECASE)

  
    texto = re.sub(r'\s{2,}', ' ', texto)


    texto = re.sub(r'(\w)-\n(\w)', r'\1\2', texto)

    return texto.strip()

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

def extrair_questoes(texto):
 
    partes = re.split(r'(?:^|\n)\s*(\d{1,3})\.\s', texto)

    questoes = []

    for i in range(1, len(partes), 2):
        numero = int(partes[i])
        conteudo = partes[i + 1]
        questoes.append((numero, conteudo.strip()))

    return questoes

def extrair_alternativas(texto):
    padrao = r'^\s*([a-e])\)\s*(.*?)(?=^\s*[a-e]\)|$)'

    matches = re.findall(padrao, texto, re.DOTALL | re.IGNORECASE | re.MULTILINE)

    alternativas = {}

    for letra, conteudo in matches:
        alternativas[letra.upper()] = conteudo.strip()

    if not alternativas:
        return texto.strip(), {}

    texto_sem_alternativas = re.sub(
        r'^\s*[a-e]\)\s*.*?(?=^\s*[a-e]\)|$)',
        '',
        texto,
        flags=re.IGNORECASE | re.DOTALL | re.MULTILINE
    )

    enunciado = texto_sem_alternativas.strip()

    return enunciado, alternativas

def extrair_itens(texto):
    padrao = r'(I|II|III|IV)\.\s*(.*?)(?=\n\s*(I|II|III|IV)\.|$)'
    matches = re.findall(padrao, texto, re.DOTALL)

    return [
        {"item": m[0], "texto": m[1].strip()}
        for m in matches
    ]

def ler_csv_gabarito(caminho):
    gabarito = {}

    with open(caminho, "r", encoding="utf-8") as f:
        next(f)

        for linha in f:
            linha = linha.strip()
            if not linha:
                continue

            id_, resposta = linha.split(",")

            partes = id_.split("_")
            prova = partes[0]
            tipo = partes[1]
            numero = int(partes[2])

            resposta = resposta.strip().upper()

            if prova not in gabarito:
                gabarito[prova] = {}

            if tipo not in gabarito[prova]:
                gabarito[prova][tipo] = {}

            if resposta in ["NULA", "ANULADA"]:
                gabarito[prova][tipo][numero] = "ANULADA"
            else:
                gabarito[prova][tipo][numero] = resposta

    return gabarito



gabaritos = {}

for arquivo in os.listdir(PASTA_GABARITO):
    if not arquivo.endswith(".csv"):
        continue

    print(f"\n📥 Lendo gabarito CSV: {arquivo}")

    caminho = os.path.join(PASTA_GABARITO, arquivo)

    nome_prova = arquivo.split(".")[0]  # ex: pm2021
    gabaritos.update(ler_csv_gabarito(caminho))

for arquivo in os.listdir(PASTA_TXT):
    if not arquivo.endswith(".txt"):
        continue

    print(f"\n📄 Processando: {arquivo}")

    caminho = os.path.join(PASTA_TXT, arquivo)
    texto = ler_txt(caminho)
    questoes = extrair_questoes(texto)

    nome_prova = arquivo.split("_")[0]
    tipo = arquivo.split("_")[1].replace(".txt", "").lower()

    gabarito_prova = gabaritos.get(nome_prova, {}).get(tipo, {})

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

        # 🔥 verifica prova + tipo
        if nome_prova not in gabaritos or tipo not in gabaritos[nome_prova]:
            print(f"❌ SEM TIPO NO GABARITO -> {nome_prova}_{tipo}")
            continue

        gabarito_prova = gabaritos[nome_prova][tipo]

        
        if numero not in gabarito_prova:
            print(f"❌ REMOVIDA (sem gabarito) -> {nome_prova}_{tipo} | Q{numero}")
            questoes_removidas.append((nome_prova, tipo, numero))
            continue

      
        if gabarito_prova[numero] == "ANULADA":
            print(f"⚠️ ANULADA -> {nome_prova}_{tipo} | Q{numero}")
            continue

        enunciado, alternativas = extrair_alternativas(conteudo)

        
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

enunciados_vistos = {}
dados_unicos = []
duplicadas = []

def normalizar_texto(t):
    t = t.lower().strip()
    t = re.sub(r'\s+', ' ', t)
    return t

for item in dados:
    enunciado_norm = normalizar_texto(item["enunciado"])

    if enunciado_norm in enunciados_vistos:
        duplicadas.append({
            "removida": item["id"],
            "mantida": enunciados_vistos[enunciado_norm]["id"],
            "enunciado": item["enunciado"][:120]  # preview
        })
    else:
        enunciados_vistos[enunciado_norm] = item
        dados_unicos.append(item)

dados = dados_unicos


print("\n🔁 DUPLICADAS REMOVIDAS:", len(duplicadas))

for d in duplicadas:
    print("\n------------------------")
    print(f"❌ Removida: {d['removida']}")
    print(f"✅ Mantida:  {d['mantida']}")
    print(f"📝 Enunciado: {d['enunciado']}...")

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