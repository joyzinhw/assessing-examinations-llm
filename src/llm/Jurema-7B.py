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

import json
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# ======================
# 🔹 CONFIGURAÇÕES
# ======================
DATASET_PATH = "src/dataset/dataset.json"  # caminho local do dataset
SAIDA_PATH = "src/dataset/respostas_jurema.json"
MODEL_ID = "Jurema-br/Jurema-7B"

# ======================
# 🔹 CARREGAR MODELO
# ======================
print("🔄 Carregando modelo...")

device = "cuda" if torch.cuda.is_available() else "cpu"
model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    device_map="auto" if device=="cuda" else None,
    torch_dtype=torch.bfloat16 if device=="cuda" else torch.float32,
    low_cpu_mem_usage=True
)

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

print("✅ Modelo carregado!")

# ======================
# 🔹 LER DATASET
# ======================
with open(DATASET_PATH, "r", encoding="utf-8") as f:
    dataset = json.load(f)

print(f"Dataset carregado: {len(dataset)} questões")

# ======================
# 🔹 FUNÇÕES DE PROMPT
# ======================
def montar_prompt(questao):
    system_prompt = (
        "Você é um especialista em Direito brasileiro. "
        "Responda apenas com a letra correta (A-E), sem explicações."
    )

    user_content = f"QUESTÃO:\n{questao['enunciado']}\n"

    if "itens" in questao and questao["itens"]:
        user_content += "\nITENS:\n"
        for item in questao["itens"]:
            user_content += f"{item['item']}) {item['texto']}\n"

    user_content += "\nALTERNATIVAS:\n"
    for letra, texto in questao["alternativas"].items():
        user_content += f"{letra}) {texto}\n"

    user_content += "\nResposta (A-E):"

    return user_content

def extrair_letra(texto_gerado):
    limpo = texto_gerado.strip().upper()
    for letra in ["A", "B", "C", "D", "E"]:
        if limpo.startswith(letra):
            return letra
    # Último recurso
    for char in reversed(limpo):
        if char in "ABCDE":
            return char
    return "ERRO"

# ======================
# 🔹 INFERÊNCIA
# ======================
print("🚀 Iniciando inferência...")

resultados = []

for i, questao in enumerate(dataset):
    prompt = montar_prompt(questao)

    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1024).to(model.device)

    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=5,
            do_sample=False
        )

    resposta_bruta = tokenizer.decode(output[0], skip_special_tokens=True)
    letra = extrair_letra(resposta_bruta)

    resultados.append({"id": questao["id"], "resposta": letra})
    print(f"[{i+1}/{len(dataset)}] ID: {questao['id']} -> {letra}")

# ======================
# 🔹 SALVAR RESULTADOS
# ======================
with open(SAIDA_PATH, "w", encoding="utf-8") as f:
    json.dump(resultados, f, ensure_ascii=False, indent=2)

print(f"\n✅ Respostas salvas em: {SAIDA_PATH}")