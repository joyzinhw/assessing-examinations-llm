import re

INPUT = "src/txt/pm2021_c.txt"
OUTPUT = "src/txt/pm2021_c_limpo.txt"


def pre_formatar(texto):
    texto = re.sub(r'\s+(\d{1,3}\.)', r'\n\1', texto)
    texto = re.sub(r'\s+([a-e]\))', r'\n\1', texto)
    return texto


def remover_lixo(texto):
    linhas = texto.split("\n")
    limpo = []

    for linha in linhas:
        l = linha.strip()

        if re.search(r'CARGO:', l, re.IGNORECASE): continue
        if re.search(r'PROVA TIPO', l, re.IGNORECASE): continue
        if re.search(r'CONCURSO PÚBLICO', l, re.IGNORECASE): continue
        if re.search(r'SEJUS', l, re.IGNORECASE): continue
        if re.search(r'NOÇÕES DE DIREITO', l, re.IGNORECASE): continue
        if re.search(r'DIREITO PENAL', l, re.IGNORECASE): continue

        if re.match(r'^\d+$', l): continue
        if re.search(r'\d+CONCURSO', l): continue

        limpo.append(linha)

    return "\n".join(limpo)


def remover_links_datas(texto):
    texto = re.sub(r'https?://\S+', '', texto)
    texto = re.sub(r'\b\w+/\S+\.ghtml\S*', '', texto)
    texto = re.sub(r'\S+\.(html|ghtml)\S*', '', texto)
    texto = re.sub(r'Disponível em:.*', '', texto, flags=re.IGNORECASE)
    texto = re.sub(r'Acesso em:.*', '', texto, flags=re.IGNORECASE)
    texto = re.sub(r'Acesso em\s*\.*', '', texto, flags=re.IGNORECASE)
    texto = re.sub(r'\b\d{2}/\d{2}/\d{4}\b', '', texto)
    return texto


def remover_citacoes(texto):
    return re.sub(r'\([A-ZÁ-Ú][^()]{20,}\d{4}[^()]*\)', '', texto)


def corrigir_questoes(texto):
    return re.sub(r'\n\s*(\d)\s*\n\s*(\d{1,2})\.', r'\n\1\2.', texto)


def padronizar_itens(texto):
    texto = re.sub(r'\b(I{1,3}V?)\.\s*\n\s*', r'\1. ', texto)
    texto = re.sub(r'\s+(I{1,3}V?\.)', r'\n\1', texto)
    return texto


def corrigir_alternativas(texto):
    return re.sub(r'\)\s*([a-e]\))', r')\n\1', texto)


def clean_ocr(texto):
    texto = re.sub(r',\s*,+', ',', texto)
    texto = re.sub(r':\s*,+', ':', texto)
    texto = re.sub(r'\b\w+\.ghtml\b', '', texto)
    texto = re.sub(r'\b(nacional|noticia|brasil-em-constituicao)\b/?', '', texto)
    texto = re.sub(r'(\w+)-\n(\w+)', r'\1\2', texto)

    texto = re.sub(r'([A-Z])\n([a-z])', r'\1 \2', texto)
    texto = re.sub(r'([a-z])\n([a-z])', r'\1 \2', texto)

    texto = re.sub(r'\b(\w+)\s+\1\b', r'\1', texto, flags=re.IGNORECASE)

    texto = re.sub(r'\n(?!\s*(\d+\.|[a-e]\)))', ' ', texto)

    correcoes = {
        "ccomo": "como",
        "altealternativa": "alternativa",
        "rnativa": "alternativa",
        "omo": "como",
        "prcomover": "promover",
        "interes interesse": "interesse",
    }

    for errado, certo in correcoes.items():
        texto = re.sub(errado, certo, texto, flags=re.IGNORECASE)

    texto = re.sub(r' +', ' ', texto)
    texto = re.sub(r'\n+', '\n', texto)

    return texto.strip()


def split_questoes(texto):
    return re.split(r'(?=\n\d{1,3}\.\s)', texto)


def formatar_questao(q):
    q = q.strip()
    partes = re.split(r'(?=\n[a-e]\))', q)
    corpo = partes[0]
    alternativas = partes[1:]

    resultado = []
    resultado.append(corpo.strip())
    resultado.append("")

    for alt in alternativas:
        resultado.append(alt.strip())

    resultado.append("\n")

    return "\n".join(resultado)


def remover_urls_quebradas(texto):
    linhas = texto.split("\n")
    limpo = []

    for linha in linhas:
        l = linha.strip()

        if re.search(r'\d{4}/\d{2}/\d{2}', l):
            continue

        if l.count("-") >= 3:
            continue

        if "/" in l and len(l) < 120:
            continue

        if re.search(r'\.(html|ghtml)', l):
            continue

        limpo.append(linha)

    return "\n".join(limpo)


def processar():
    with open(INPUT, "r", encoding="utf-8") as f:
        texto = f.read()

    texto = pre_formatar(texto)
    texto = remover_lixo(texto)
    texto = remover_links_datas(texto)
    texto = remover_urls_quebradas(texto)
    texto = remover_citacoes(texto)
    texto = corrigir_questoes(texto)
    texto = corrigir_alternativas(texto)
    texto = clean_ocr(texto)
    texto = padronizar_itens(texto)

    questoes = split_questoes(texto)

    resultado = []
    for q in questoes:
        if q.strip():
            resultado.append(formatar_questao(q))

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write("\n".join(resultado))

    print("✔ AGORA VAI FICAR CERTO:", OUTPUT)


if __name__ == "__main__":
    processar()