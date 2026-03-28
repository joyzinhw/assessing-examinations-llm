# Extrator de Questões - Dataset PC2025

## 📋 Descrição

Este conjunto de scripts extrai questões do arquivo `dataset_pc2025.txt` e as converte para um arquivo CSV estruturado.

## ✅ O Que Foi Feito

1. **extrair_final.py** - Script principal que lê o arquivo TXT e extrai as questões
   - Extrai: ID da questão, enunciado, alternativas (A-E) e marca respostas como 0 (padrão)
   - Saída: `src/dataset/questoes.csv` com 138 questões

2. **corrigir_csv.py** - Corrige a codificação do CSV para UTF-8-BOM
   - Melhor compatibilidade com Excel
   - Resolve problemas de caracteres acentuados

3. **atualizar_gabarito.py** - Script interativo para adicionar respostas corretas
   - Permite marcar quais alternativas são corretas
   - Atualiza as colunas: resposta = 1 (correta) ou 0 (errada)

## 📊 Estrutura do CSV

O arquivo `questoes.csv` contém as seguintes colunas:

| Coluna | Descrição |
|--------|-----------|
| `id` | Identificador único (ex: `pc2025_01_pn_31`) |
| `enunciado` | Texto da questão |
| `opcao` | Alternativa (A, B, C, D ou E) |
| `texto_alternativa` | Conteúdo da alternativa |
| `resposta` | 0 (errada) ou 1 (correta) - preenchida após executar atualizar_gabarito.py |

## 🚀 Como Usar

### 1. Scripts já executados (geraram o CSV):

```bash
python extrair_final.py
python corrigir_csv.py
```

### 2. Para adicionar o gabarito:

```bash
python atualizar_gabarito.py
```

Você pode:
- Digitar uma por uma as respostas no formato `ID:RESPOSTA`
  - Exemplo: `pc2025_01_pn_31:C`
- Carregar de um arquivo de texto (digite `f` e enter)
- Digitar `sair` para finalizar

### 3. Exemplo de arquivo de gabarito (gabarito.txt):

```
pc2025_01_pn_31:C
pc2025_01_pn_32:E
pc2025_01_pn_33:B
pc2025_01_pn_34:D
pc2025_01_pn_35:C
...
```

## 📁 Arquivos Criados/Modificados

- `src/dataset/questoes.csv` - CSV com todas as questões e alternativas
- `extrair_final.py` - Script de extração
- `corrigir_csv.py` - Script de correção de encoding
- `atualizar_gabarito.py` - Script para adicionar respostas corretas
- `README_QUESTOES.md` - Este arquivo

## ✨ Características

✅ 138 questões extraídas
✅ 690 linhas (5 alternativas por questão)
✅ Codificação UTF-8-BOM (compatível com Excel)
✅ Formato CSV padrão (vírgulas, aspas onde necessário)
✅ Script auxiliar para atualizar gabarito facilmente

## ⚠️ Notas Importantes

1. A coluna `resposta` começa com valor `0` para todas as alternativas
2. Você DEVE executar `atualizar_gabarito.py` e informar as respostas corretas
3. Após marcar as respostas, apenas as alternativas corretas terão `resposta = 1`

## 🔧 Troubleshooting

Se o CSV não abrir corretamente no Excel:
1. Verifique se a codificação é UTF-8-BOM (já corrigida)
2. Tente abrir como "Delimited" e selecionar "Comma"
3. Reexecute `python corrigir_csv.py`

Se as questões não foram extraídas corretamente:
1. Verifique se `src/dataset/dataset_pc2025.txt` existe e tem conteúdo
2. Reexecute `python extrair_final.py`
3. Verifique a contagem de questões na saída do script

## 📞 Próximos Passos

1. Revisar o CSV gerado em `src/dataset/questoes.csv`
2. Obter o gabarito (respostas corretas) da prova
3. Executar `python atualizar_gabarito.py` com o gabarito
4. Usar o CSV para seus estudos, testes de LLM, etc.
