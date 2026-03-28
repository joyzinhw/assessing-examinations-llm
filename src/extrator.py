import os
import pdfplumber
from docx import Document
from tqdm import tqdm

BASE_DIR = "src/concursos"  # pasta onde estão pc2025, pm2021, pp2024
OUTPUT_DIR = "docs_provas"

os.makedirs(OUTPUT_DIR, exist_ok=True)


def extrair_texto_pdf(pdf_path):
    texto_completo = []

    try:
        with pdfplumber.open(pdf_path) as pdf:
            for pagina in pdf.pages:
                texto = pagina.extract_text()
                if texto:
                    texto_completo.append(texto)
    except Exception as e:
        print(f"Erro ao processar {pdf_path}: {e}")

    return "\n\n".join(texto_completo)


def salvar_docx(texto, caminho_saida):
    doc = Document()

    for linha in texto.split("\n"):
        doc.add_paragraph(linha)

    doc.save(caminho_saida)


def processar_pasta(concurso_path):
    provas_path = os.path.join(concurso_path, "Provas")

    if not os.path.exists(provas_path):
        return

    nome_concurso = os.path.basename(concurso_path)

    arquivos_pdf = [f for f in os.listdir(provas_path) if f.endswith(".pdf")]

    for pdf_file in tqdm(arquivos_pdf, desc=f"Processando {nome_concurso}"):
        pdf_path = os.path.join(provas_path, pdf_file)

        texto = extrair_texto_pdf(pdf_path)

        nome_saida = pdf_file.replace(".pdf", ".docx")
        caminho_saida = os.path.join(OUTPUT_DIR, f"{nome_concurso}_{nome_saida}")

        salvar_docx(texto, caminho_saida)


def main():
    pastas = ["pc2025", "pm2021", "pp2024"]

    for pasta in pastas:
        caminho = os.path.join(BASE_DIR, pasta)

        if os.path.exists(caminho):
            processar_pasta(caminho)
        else:
            print(f"Pasta não encontrada: {pasta}")


if __name__ == "__main__":
    main()