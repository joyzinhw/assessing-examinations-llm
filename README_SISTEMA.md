# 📚 Sistema de Extração de Questões de Provas

Um sistema modular e extensível para extrair questões de arquivos TXT de provas e convertê-las para CSV estruturado.

## ✨ Características

- ✅ **Modularizado**: Classes bem definidas e reutilizáveis
- ✅ **Extensível**: Fácil adicionar novos tipos de provas
- ✅ **Documentado**: Código comentado e com exemplos
- ✅ **Robusto**: Tratamento de erros e validações
- ✅ **Simples**: Interface de linha de comando clara

## 📁 Estrutura dos Arquivos

```
assessing-examinations-llm/
├── config_provas.py              # Configuração de provas disponíveis
├── extrator_questoes.py          # Módulo de extração de questões
├── atualizador_gabarito.py       # Módulo de atualização de gabarito
├── main.py                        # Script principal (orquestra)
├── gerar_gabarito_exemplo.py     # Gera arquivo de exemplo
│
└── src/dataset/
    ├── dataset_pc2025.txt        # Arquivo TXT com questões (entrada)
    ├── questoes_pc2025.csv       # CSV gerado (saída)
    ├── gabarito_pc2025.txt       # Arquivo com respostas corretas
    ├── dataset_pm2025.txt        # (Opcional) Outro tipo de prova
    └── questoes_pm2025.csv       # (Opcional) CSV da outra prova
```

## 🚀 Guia de Uso

### 1️⃣ Extrair Questões

Extrai um arquivo TXT e gera um CSV com as questões:

```bash
python main.py extrair pc2025
```

Saída esperada:
- `src/dataset/questoes_pc2025.csv` com 138 questões

### 2️⃣ Gerar Arquivo de Gabarito (Opcional)

Cria um arquivo template para você preencher com as respostas:

```bash
python gerar_gabarito_exemplo.py
```

Isso cria `src/dataset/gabarito_pc2025_exemplo.txt` que você pode editar.

### 3️⃣ Atualizar Gabarito

Marca as respostas corretas no CSV:

```bash
python main.py gabarito pc2025 src/dataset/gabarito_pc2025.txt
```

Após executar:
- A coluna `resposta` será atualizada (1 = correta, 0 = errada)
- Um relatório mostra quantas questões têm gabarito

### 4️⃣ Listar Provas Disponíveis

```bash
python main.py listar
```

### 5️⃣ Ver Ajuda

```bash
python main.py ajuda
```

## 📋 Formato do Arquivo de Gabarito

Crie um arquivo de texto simples (`gabarito_pc2025.txt`) com o formato:

```
# Comentários começam com #
# Linhas em branco são ignoradas

pc2025_01_pn_31:C
pc2025_01_pn_32:E
pc2025_01_pn_33:B
pc2025_01_pn_34:D
pc2025_01_pn_35:C
pc2025_02_pn_31:A
pc2025_02_pn_32:E
...
```

**Formato esperado**: `ID_QUESTAO:RESPOSTA`
- `ID_QUESTAO`: Identificador único (ex: `pc2025_01_pn_31`)
- `RESPOSTA`: Uma das letras A, B, C, D ou E

## 📊 Formato do CSV Gerado

O arquivo CSV tem a seguinte estrutura:

```csv
id,enunciado,opcao,texto_alternativa,resposta
"pc2025_01_pn_31","João, reincidente...",A,"simples, com a incidência...",0
"pc2025_01_pn_31","João, reincidente...",B,"qualificado, com...",0
"pc2025_01_pn_31","João, reincidente...",C,"simples, com a...",1
"pc2025_01_pn_31","João, reincidente...",D,"qualificado, sem...",0
"pc2025_01_pn_31","João, reincidente...",E,"simples, sem...",0
"pc2025_01_pn_32","Caio, servidor...",A,"não responderá...",0
...
```

Cada questão ocupa **5 linhas** (uma por alternativa).

## ➕ Adicionar Nova Prova (PM2025)

### Passo 1: Adicionar em `config_provas.py`

```python
PROVAS_DISPONIVEIS = {
    'pc2025': ConfigProva(...),  # Já existe
    'pm2025': ConfigProva(       # Adicione isso
        nome='Polícia Militar 2025',
        codigo_prefixo='pm2025',
        arquivo_entrada='dataset_pm2025.txt',
        arquivo_saida='questoes_pm2025.csv',
        descricao='Prova de Polícia Militar de 2025'
    ),
}
```

### Passo 2: Colocar arquivo TXT

Coloque o arquivo `dataset_pm2025.txt` em `src/dataset/`

### Passo 3: Extrair

```bash
python main.py extrair pm2025
```

### Passo 4: Atualizar gabarito (se quiser)

```bash
python main.py gabarito pm2025 src/dataset/gabarito_pm2025.txt
```

É isso! O sistema funcionará automaticamente.

## 🏗️ Arquitetura de Módulos

### `config_provas.py`

Define as configurações de cada tipo de prova disponível.

```python
ConfigProva = Dataclass com:
  - nome: Nome da prova
  - codigo_prefixo: Prefixo do código (pc2025, pm2025, etc)
  - arquivo_entrada: Arquivo TXT
  - arquivo_saida: Arquivo CSV gerado
  - descricao: Descrição para logs
```

### `extrator_questoes.py`

Extrai questões de um arquivo TXT.

```python
class ExtratorQuestoesTXT:
  - __init__(caminho_arquivo)
  - extrair() -> List[Questao]
  - para_csv(caminho_saida)
```

### `atualizador_gabarito.py`

Atualiza os gabaritos no CSV.

```python
class AtualizadorGabarito:
  - __init__(caminho_csv)
  - carregar_gabarito(caminho_arquivo)
  - atualizar() -> Tuple[atualizado, nao_encontrado]
  - gerar_relatorio()
```

### `main.py`

Orquestra os módulos e fornece interface CLI.

```python
Funções:
  - extrair_questoes(tipo_prova)
  - atualizar_gabarito(tipo_prova, arquivo_gabarito)
  - listar_provas()
  - mostrar_ajuda()
```

## 🔍 Exemplos de Uso Completo

### Cenário 1: Extrair e atualizar PC2025

```bash
# 1. Esperar que dataset_pc2025.txt esteja em src/dataset/
# 2. Extrair questões
python main.py extrair pc2025

# 3. Gerar arquivo de exemplo
python gerar_gabarito_exemplo.py

# 4. Editar src/dataset/gabarito_pc2025.txt com as respostas corretas

# 5. Atualizar gabarito
python main.py gabarito pc2025 src/dataset/gabarito_pc2025.txt
```

### Cenário 2: Adicionar PM2025

```bash
# 1. Editar config_provas.py e adicionar pm2025
# 2. Colocar dataset_pm2025.txt em src/dataset/
# 3. Extrair
python main.py extrair pm2025

# 4. Atualizar gabarito (se quiser)
python main.py gabarito pm2025 src/dataset/gabarito_pm2025.txt
```

## ⚠️ Notas Importantes

1. **Codificação**: Todos os arquivos usam UTF-8 com BOM para compatibilidade com Excel
2. **Resposta padrão**: Todas as alternativas começam com `resposta = 0`
3. **Gabarito obrigatório?**: Não. Você pode deixar as respostas com 0 se quiser
4. **Edição manual do CSV**: Você pode editar o CSV manualmente se preferir não usar o atualizador

## 🆘 Troubleshooting

### "Arquivo não encontrado"

Certifique-se que:
- O arquivo TXT está em `src/dataset/`
- O caminho está correto em `config_provas.py`
- O arquivo tem permissão de leitura

### "Nenhuma questão foi extraída"

Verifique:
- O formato do arquivo TXT (deve ter "Código:", números de questão, alternativas)
- Se o arquivo não está vazio
- Se a codificação é UTF-8

### "Questões sem gabarito"

Isso é normal se você não informou gabarito para todas. Você pode:
- Editar o arquivo de gabarito e adicionar as respostas faltantes
- Editar o CSV manualmente
- Deixar em branco (padrão = 0)

## 📞 Suporte

Se encontrar problemas:

1. Verifique os arquivos de entrada
2. Execute com verbosidade (ver saída do script)
3. Confira o formato esperado
4. Verifique se todos os arquivos estão em UTF-8

---

**Autor**: Sistema de Extração de Questões
**Versão**: 1.0
**Data**: Março de 2026
