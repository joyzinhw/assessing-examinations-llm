import os
import re
import json

PASTA = "src/txt"
SAIDA = "src/dataset/dataset.json"

dados = []

def ler_txt(caminho):
    with open(caminho, "r", encoding="utf-8") as f:
        return f.read()


def extrair_questoes(texto):
    partes = re.split(r'\n\s*(\d{1,3})\.\s', texto)

    questoes = []

    for i in range(1, len(partes), 2):
        numero = int(partes[i])
        conteudo = partes[i+1]
        questoes.append((numero, conteudo.strip()))

    return questoes


def extrair_itens(texto):
    padrao = r'\b(I{1,3}V?)\.\s*(.*?)\s*(?=(I{1,3}V?\.)|$)'
    itens = re.findall(padrao, texto, re.DOTALL)

    resultado = []

    for item in itens:
        resultado.append({
            "item": item[0],
            "texto": item[1].strip()
        })

    return resultado


def extrair_alternativas(texto):
    partes = re.split(r'\n([a-e])\)\s', texto, flags=re.IGNORECASE)

    if len(partes) < 3:
        return texto.strip(), {}

    enunciado = partes[0].strip()
    alternativas = {}

    for i in range(1, len(partes), 2):
        letra = partes[i].upper()
        conteudo = partes[i+1].strip()
        alternativas[letra] = conteudo

    return enunciado, alternativas


for arquivo in os.listdir(PASTA):
    if not arquivo.endswith(".txt"):
        continue

    caminho = os.path.join(PASTA, arquivo)
    print(f"Processando: {arquivo}")

    texto = ler_txt(caminho)

    # 🔥 se quiser usar sua limpeza OCR:
    # texto = clean_ocr(texto)

    questoes = extrair_questoes(texto)

    nome_prova = arquivo.split("_")[0]
    tipo = arquivo.split("_")[1].replace(".txt", "").lower()

    for numero, conteudo in questoes:

        enunciado, alternativas = extrair_alternativas(conteudo)

        # ignora coisas que não são questões válidas
        if len(alternativas) < 2:
            continue

        itens = extrair_itens(enunciado)

        item = {
            "id": f"{nome_prova}_{tipo}_{numero}",
            "numero": numero,
            "enunciado": enunciado,
            "alternativas": alternativas
        }

        if len(itens) > 0:
            item["itens"] = itens

        dados.append(item)


with open(SAIDA, "w", encoding="utf-8") as f:
    json.dump(dados, f, ensure_ascii=False, indent=2)

print("✅ Total de questões:", len(dados))