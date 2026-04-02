import json
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

DATASET_PATH = "src/dataset/dataset.json"
SAIDA_PATH = "src/dataset/respostas.json"

print("🔄 Carregando modelo llama...")

model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Meta-Llama-3-8B-Instruct",
    device_map="auto",
    torch_dtype=torch.bfloat16
)

tokenizer = AutoTokenizer.from_pretrained(
    "meta-llama/Meta-Llama-3-8B-Instruct"
)

print("✅ Modelo carregado!")


with open(DATASET_PATH, "r", encoding="utf-8") as f:
    dataset = json.load(f)


def montar_prompt(questao):
    system = """Você é um especialista em Direito brasileiro.
Responda corretamente questões de múltipla escolha."""

    user = """
Responda a questão e diga apenas a letra correta (A, B, C, D ou E).

REGRAS:
- Analise todo o enunciado
- Se houver itens (I, II, III...), analise TODOS
- NÃO ignore os itens
- NÃO explique
- Responda apenas com uma letra
"""

    # Enunciado
    user += f"\nQUESTÃO:\n{questao['enunciado']}\n"

    # Itens
    if "itens" in questao and questao["itens"]:
        user += "\nITENS:\n"
        for item in questao["itens"]:
            user += f"{item['item']}) {item['texto']}\n"

    # Alternativas
    user += "\nALTERNATIVAS:\n"
    for letra, texto in questao["alternativas"].items():
        user += f"{letra}) {texto}\n"

    user += "\nResposta (apenas uma letra):"

    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": user}
    ]

    return tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )


def extrair_letra(texto):
    texto = texto.upper()

    for l in ["A", "B", "C", "D", "E"]:
        if l in texto:
            return l

    return "ERRO"


print("🚀 Iniciando inferência...")

resultados = []

for i, questao in enumerate(dataset):
    prompt = montar_prompt(questao)

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=3,   # 🔥 menor = mais preciso
            do_sample=False,
            temperature=0.0
        )

    resposta_bruta = tokenizer.decode(output[0], skip_special_tokens=True)

    # 🔥 pega só o final
    resposta_bruta = resposta_bruta.split("assistant")[-1]

    letra = extrair_letra(resposta_bruta)

    resultados.append({
        "id": questao["id"],
        "resposta": letra
    })

    print(f"[{i+1}/{len(dataset)}] {questao['id']} -> {letra}")

# ======================
# 🔹 SALVAR
# ======================
with open(SAIDA_PATH, "w", encoding="utf-8") as f:
    json.dump(resultados, f, ensure_ascii=False, indent=2)

print(f"\n✅ Respostas salvas em: {SAIDA_PATH}")

