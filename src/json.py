

#transforma cvs em json todo organizado
import csv
import json

dados = {}

with open("src/dataset/cvs-test.csv", encoding="utf-8") as f:
    reader = csv.reader(f, delimiter=",", quotechar='"')

    next(reader)  

    for row in reader:
        if len(row) < 5:
            continue

        id_, enunciado, alternativa, texto_alt, label = row[:5]

        try:
            label = int(label)
        except:
            continue

        if id_ not in dados:
            dados[id_] = {
                "id": id_,
                "pergunta": enunciado,
                "alternativas": {},
                "correta": None
            }

        dados[id_]["alternativas"][alternativa] = texto_alt

        if label == 1:
            dados[id_]["correta"] = alternativa

resultado = [v for v in dados.values() if v["correta"]]

with open("src/dataset/dataset.json", "w", encoding="utf-8") as f:
    json.dump(resultado, f, ensure_ascii=False, indent=2)

print("Total de questões:", len(resultado))