import json
import csv
import os

def json_to_csv():
    """
    Converte dataset.json para CSV com o seguinte formato:
    ID, enunciado, opcao, texto_alternativa, resposta (0 ou 1)
    """
    
    # Caminho dos arquivos
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_path = os.path.join(base_path, 'src', 'dataset', 'dataset.json')
    csv_path = os.path.join(base_path, 'src', 'dataset', 'questoes.csv')
    
    # Ler o JSON
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Criar o CSV
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['id', 'enunciado', 'opcao', 'texto_alternativa', 'resposta']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        # Processar cada questão
        for questao in data:
            questao_id = questao['id']
            enunciado = questao['pergunta']
            resposta_correta = questao['correta']
            alternativas = questao['alternativas']
            
            # Escrever uma linha para cada alternativa
            for opcao, texto in alternativas.items():
                resposta = 1 if opcao == resposta_correta else 0
                
                writer.writerow({
                    'id': questao_id,
                    'enunciado': enunciado,
                    'opcao': opcao,
                    'texto_alternativa': texto,
                    'resposta': resposta
                })
    
    print(f"✓ CSV criado com sucesso em: {csv_path}")
    print(f"✓ Total de questões processadas: {len(data)}")
    print(f"✓ Total de linhas no CSV: {len(data) * 5}")  # 5 alternativas por questão

if __name__ == "__main__":
    json_to_csv()
