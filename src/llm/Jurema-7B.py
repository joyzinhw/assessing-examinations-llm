import json
import torch
import re
from transformers import AutoModelForCausalLM, AutoTokenizer

# ======================
# 🔹 CONFIG
# ======================
DATASET_PATH = "src/dataset/dataset.json"
SAIDA_PATH = "src/dataset/respostas.json"

# ======================
# 🔹 CARREGAR MODELO
# ======================
print("🔄 Carregando modelo...")

model = AutoModelForCausalLM.from_pretrained(
    "Jurema-br/Jurema-7B",
    device_map="auto",
    torch_dtype=torch.bfloat16,
    token=True
)

tokenizer = AutoTokenizer.from_pretrained(
    "Jurema-br/Jurema-7B",
    token=True
)

print("✅ Modelo carregado!")

# ======================
# 🔹 LER DATASET
# ======================
with open(DATASET_PATH, "r", encoding="utf-8") as f:
    dataset = json.load(f)

# ======================
# 🔹 PROMPT MELHORADO
# ======================
def montar_prompt(questao):
    prompt = """
Responda a questão de múltipla escolha.

IMPORTANTE:
- Retorne SOMENTE uma letra (A, B, C, D ou E)
- NÃO escreva nenhuma palavra além da letra
- NÃO explique
- NÃO repita o enunciado

Formato da resposta:
A

"""

    prompt += f"\nQUESTÃO:\n{questao['enunciado']}\n"

    if "itens" in questao and questao["itens"]:
        prompt += "\nITENS:\n"
        for item in questao["itens"]:
            prompt += f"{item['item']}) {item['texto']}\n"

    prompt += "\nALTERNATIVAS:\n"
    for letra, texto in questao["alternativas"].items():
        prompt += f"{letra}) {texto}\n"

    prompt += "\nResposta:"

    return prompt

# ======================
# 🔹 EXTRAÇÃO CORRETA DA LETRA
# ======================
def extrair_letra(texto):
    texto = texto.upper()

    # pega apenas letra isolada (A B C D E)
    match = re.search(r'\b([ABCDE])\b', texto)
    if match:
        return match.group(1)

    return "ERRO"

# ======================
# 🔹 INFERÊNCIA
# ======================
print("🚀 Iniciando inferência...")

resultados = []

for i, questao in enumerate(dataset):
    prompt = montar_prompt(questao)

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=1024
    ).to(model.device)

    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=5,
            do_sample=False  # 🔥 determinístico (ideal pra prova)
        )

    resposta_bruta = tokenizer.decode(output[0], skip_special_tokens=True)

    # pega só depois de "Resposta:"
    if "Resposta:" in resposta_bruta:
        resposta_bruta = resposta_bruta.split("Resposta:")[-1]

    letra = extrair_letra(resposta_bruta)

    resultados.append({
        "id": questao["id"],
        "resposta": letra
    })

    print(f"[{i+1}/{len(dataset)}] {questao['id']} -> {letra}")

# ======================
# 🔹 SALVAR RESULTADOS
# ======================
with open(SAIDA_PATH, "w", encoding="utf-8") as f:
    json.dump(resultados, f, ensure_ascii=False, indent=2)

print(f"\n✅ Respostas salvas em: {SAIDA_PATH}")

# ======================
# 🔹 AVALIAÇÃO
# ======================
acertos = 0
total = 0

for questao, resp in zip(dataset, resultados):
    if "gabarito" in questao:
        total += 1
        if questao["gabarito"] == resp["resposta"]:
            acertos += 1

if total > 0:
    acc = (acertos / total) * 100
    print(f"\n🎯 Acurácia: {acc:.2f}% ({acertos}/{total})")
else:
    print("\nℹ️ Dataset sem gabarito para avaliação.")