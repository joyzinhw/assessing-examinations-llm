import re
import pandas as pd

def extrair_questoes(src\dataset\dataset_pc2025.txt):
    with open(src\dataset\dataset_pc2025.txt, 'r', encoding='utf-8') as f:
        texto = f.read()

    # Padrão para separar as questões baseando-se no cabeçalho 'Código:'
    # Captura o Código, o Número da Questão, o Enunciado e as Alternativas
    padrao = r"Código:\s*(?P<id>[\w_]+)\s*\n(?P<numero>\d+)\n(?P<corpo>.*?)\n\(A\)(?P<a>.*?)\n\(B\)(?P<b>.*?)\n\(C\)(?P<c>.*?)\n\(D\)(?P<d>.*?)\n\(E\)(?P<e>.*?)(?=\nCódigo:|\n...prova|\Z)"
    
    questoes = []
    
    # O re.DOTALL permite que o '.' capture quebras de linha no enunciado
    for match in re.finditer(padrao, texto, re.DOTALL):
        dados = match.groupdict()
        
        # Limpeza simples de espaços extras e quebras de linha indevidas
        item = {
            "ID": dados['id'].strip(),
            "Numero": dados['numero'].strip(),
            "Enunciado": dados['corpo'].strip().replace('\n', ' '),
            "Alternativa_A": dados['a'].strip().replace('\n', ' '),
            "Alternativa_B": dados['b'].strip().replace('\n', ' '),
            "Alternativa_C": dados['c'].strip().replace('\n', ' '),
            "Alternativa_D": dados['d'].strip().replace('\n', ' '),
            "Alternativa_E": dados['e'].strip().replace('\n', ' '),
            "Gabarito": "" # Espaço para você preencher manualmente ou via script de gabaritos
        }
        questoes.append(item)
    
    return pd.DataFrame(questoes)

# Execução
df = extrair_questoes('questoes_brutas.txt')
df.to_csv('dataset_concursos_pi.csv', index=False, encoding='utf-8-sig')
print(f"Dataset criado com {len(df)} questões!")