import os
import json
import pandas as pd

# 📁 Caminho dos gabaritos
CAMINHO_GABARITOS = "src/gabaritos"

# 📄 Arquivo JSON com respostas do modelo
ARQUIVO_JSON = "src/dataset/respostas.json"


def carregar_gabaritos(caminho):
    """
    Lê todos os CSVs e junta em um dicionário: {id: resposta}
    """
    gabarito = {}

    for arquivo in os.listdir(caminho):
        if arquivo.endswith(".csv"):
            caminho_arquivo = os.path.join(caminho, arquivo)
            df = pd.read_csv(caminho_arquivo)

            for _, row in df.iterrows():
                gabarito[row["id"]] = str(row["resposta"]).strip().upper()

    return gabarito


def carregar_respostas_json(caminho_json):
    """
    Lê o JSON com respostas do modelo
    """
    with open(caminho_json, "r", encoding="utf-8") as f:
        dados = json.load(f)

    respostas = {}
    for item in dados:
        respostas[item["id"]] = item["resposta"].strip().upper()

    return respostas


def comparar_respostas(gabarito, respostas_modelo):
    """
    Compara respostas e gera estatísticas
    """
    acertos = 0
    erros = 0
    nao_encontradas = 0

    detalhes = []

    for id_pergunta, resposta_modelo in respostas_modelo.items():
        if id_pergunta not in gabarito:
            nao_encontradas += 1
            detalhes.append((id_pergunta, resposta_modelo, "N/A", "SEM GABARITO"))
            continue

        resposta_correta = gabarito[id_pergunta]

        if resposta_modelo == resposta_correta:
            acertos += 1
            status = "ACERTO"
        else:
            erros += 1
            status = "ERRO"

        detalhes.append((id_pergunta, resposta_modelo, resposta_correta, status))

    total = acertos + erros

    acuracia = acertos / total if total > 0 else 0

    return {
        "acertos": acertos,
        "erros": erros,
        "nao_encontradas": nao_encontradas,
        "total_avaliado": total,
        "acuracia": acuracia,
        "detalhes": detalhes
    }


def salvar_resultado(resultado, arquivo_saida="resultado.csv"):
    """
    Salva os detalhes da comparação em CSV
    """
    df = pd.DataFrame(
        resultado["detalhes"],
        columns=["id", "resposta_modelo", "resposta_correta", "status"]
    )

    df.to_csv(arquivo_saida, index=False)
    print(f"📄 Resultado salvo em: {arquivo_saida}")


def main():
    print("🔄 Carregando gabaritos...")
    gabarito = carregar_gabaritos(CAMINHO_GABARITOS)

    print("🔄 Carregando respostas do JSON...")
    respostas_modelo = carregar_respostas_json(ARQUIVO_JSON)

    print("🔄 Comparando...")
    resultado = comparar_respostas(gabarito, respostas_modelo)

    print("\n📊 RESULTADO FINAL")
    print(f"✔️ Acertos: {resultado['acertos']}")
    print(f"❌ Erros: {resultado['erros']}")
    print(f"⚠️ Sem gabarito: {resultado['nao_encontradas']}")
    print(f"📈 Acurácia: {resultado['acuracia']:.2%}")

    salvar_resultado(resultado)


if __name__ == "__main__":
    main()