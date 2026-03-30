# pip install python-docx
# Código para converter um arquivo .docx em um arquivo .csv, extraindo as respostas de acordo com o formato especificado. O script lê o documento, identifica os tipos de questões e extrai as respostas, formatando-as em um CSV com um ID específico para cada questão.
import os
import csv
from docx import Document
from docx import Document
import csv
import re

def word_para_csv(caminho_docx, caminho_csv):
    doc = Document(caminho_docx)

    linhas = []
    tipo_atual = None

    # Regex para capturar "01 B"
    padrao = re.compile(r'(\d{2})\s*([A-E])')

    for paragrafo in doc.paragraphs:
        texto = paragrafo.text.strip()

        # Detecta o tipo
        if "TIPO" in texto:
            tipo_atual = texto.split()[-1]  # pega 01, 02, etc.
            continue

        # Extrai respostas
        matches = padrao.findall(texto)

        for numero, resposta in matches:
            # Formato do ID (ajuste aqui se quiser mudar)
            id_questao = f"pc2025_{tipo_atual.lower()}_{int(numero)}"
            linhas.append([id_questao, resposta])

    # Escreve o CSV
    with open(caminho_csv, mode='w', newline='', encoding='utf-8') as arquivo_csv:
        writer = csv.writer(arquivo_csv)
        writer.writerow(["id", "resposta"])  # cabeçalho
        writer.writerows(linhas)

    print("CSV gerado com sucesso!")


# USO
word_para_csv("src/gabaritos/gabarito_provas.docx", "src/gabaritos/pc2025_gabarito.csv")