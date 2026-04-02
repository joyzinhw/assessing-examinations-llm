import json
import torch
import re
from transformers import AutoModelForCausalLM, AutoTokenizer

# ======================
# 🔹 CONFIG
# ======================
DATASET_PATH = "src/dataset/dataset.json"
SAIDA_PATH = "src/dataset/respostas2.json"

# ======================
# 🔹 CARREGAR MODELO
# ======================
print("🔄 Carregando modelo Qwen...")

model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen2.5-7B-Instruct",
    device_map="auto",
    torch_dtype=torch.bfloat16
)

tokenizer = AutoTokenizer.from_pretrained(
    "Qwen/Qwen2.5-7B-Instruct"
)

print("✅ Modelo carregado!")

# ======================
# 🔹 LER DATASET
# ======================
with open(DATASET_PATH, "r", encoding="utf-8") as f:
    dataset = json.load(f)

# ======================
# 🔹 NORMALIZAR DATASET (🔥 ESSENCIAL)
# ======================
def normalizar_dataset(dataset):
    resultado = []

    for item in dataset:
        if isinstance(item, list):
            resultado.extend(item)
        elif isinstance(item, dict):
            resultado.append(item)
        else:
            print("⚠️ Ignorado:", item)

    return resultado

dataset = normalizar_dataset(dataset)

# ======================
# 🔹 CORRIGIR ITENS MAL FORMATADOS
# ======================
def corrigir_itens(questao):
    if "itens" not in questao or not questao["itens"]:
        return questao

    ultimo = questao["itens"][-1]["texto"]

    if "Assinale" in ultimo:
        partes = ultimo.split("Assinale", 1)

        questao["itens"][-1]["texto"] = partes[0].strip()
        questao["enunciado"] += "\nAssinale " + partes[1].strip()

    return questao

# ======================
# 🔹 PROMPT MELHORADO
# ======================
def montar_prompt(questao):
    if not isinstance(questao, dict):
        return None

    if "enunciado" not in questao or "alternativas" not in questao:
        return None

    questao = corrigir_itens(questao)

    system = """Você é um especialista em Direito brasileiro e concursos públicos."""

    user = """Responda a questão de múltipla escolha. 
    
    INSTRUÇÕES: 
    - Leia atentamente o enunciado - Se houver itens (I, II, III...), analise TODOS antes de decidir 
    - Determine mentalmente quais estão corretos 
    - NÃO explique 
    - Responda apenas com uma letra (A, B, C, D ou E) """
    
#     user = """Responda a questão de múltipla escolha.

# INSTRUÇÕES IMPORTANTES:
# - Leia o enunciado com atenção
# - Identifique o tema jurídico (Constitucional, Administrativo, Penal, etc.)
# - Baseie-se na legislação brasileira (especialmente Constituição e leis)
# - Analise TODAS as alternativas comparando com a regra correta
# - Elimine alternativas parcialmente corretas ou com erros sutis
# - Cuidado com prazos, exceções e termos técnicos (pegadinhas)
# - NÃO escolha a alternativa apenas por parecer correta — verifique se está totalmente correta

# REGRAS DE RESPOSTA:
# - NÃO explique
# - NÃO justifique
# - Responda apenas com uma letra (A, B, C, D ou E)
# """

    # Enunciado
    user += f"\nQUESTÃO:\n{questao['enunciado']}\n"

    # Itens (se existirem)
    if questao.get("itens"):
        user += "\nITENS:\n"
        for item in questao["itens"]:
            user += f"{item.get('item', '?')}) {item.get('texto', '')}\n"

    # Alternativas
    user += "\nALTERNATIVAS:\n"
    for letra, texto in questao["alternativas"].items():
        user += f"{letra}) {texto}\n"

    user += "\nResposta:"

    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": user}
    ]

    return tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

# ======================
# 🔹 EXTRAIR LETRA (🔥 MELHORADO)
# ======================
def extrair_letra(texto):
    texto = texto.strip().upper()

    match = re.search(r"\b([ABCDE])\b", texto)
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

    if not prompt:
        print(f"⚠️ Questão inválida: {questao}")
        continue

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=2,      # 🔥 mais restrito
            do_sample=False,
            temperature=0.0
        )

    resposta_bruta = tokenizer.decode(output[0], skip_special_tokens=True)

    # pega só resposta final
    resposta_bruta = resposta_bruta.split("assistant")[-1].strip()

    letra = extrair_letra(resposta_bruta)

    resultados.append({
        "id": questao.get("id", f"q_{i}"),
        "resposta": letra
    })

    print(f"[{i+1}/{len(dataset)}] {questao.get('id')} -> {letra}")

# ======================
# 🔹 SALVAR
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
    print("\nℹ️ Dataset sem gabarito.")      