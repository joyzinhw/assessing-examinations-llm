# 📚 Referência Completa de Scripts

## 🎯 Mapa de Scripts

```
assessing-examinations-llm/
├── main.py                      ⭐ SCRIPT PRINCIPAL - inicie aqui
├── config_provas.py             📋 Define as provas disponíveis
├── extrator_questoes.py         📖 Extrai questões do TXT
├── atualizador_gabarito.py      ✏️ Atualiza respostas no CSV
├── gerar_gabarito_exemplo.py    📝 Gera template de gabarito
├── README_SISTEMA.md            📘 Documentação completa
├── RESUMO_REFATORACAO.md        🔄 Resumo das mudanças
└── REFERENCIA_SCRIPTS.md        📚 Este arquivo
```

---

## 1️⃣ `main.py` ⭐ COMECE AQUI

**O que faz**: Orquestra todo o sistema com interface CLI

**Como usar**:
```bash
python main.py                          # Mostra ajuda
python main.py listar                   # Lista provas
python main.py extrair pc2025           # Extrai questões
python main.py gabarito pc2025 arq.txt  # Atualiza gabarito
python main.py ajuda                    # Mostra ajuda detalhada
```

**Funções principais**:
- `main()` - Entry point
- `extrair_questoes(tipo_prova)` - CLI para extração
- `atualizar_gabarito(tipo_prova, arquivo)` - CLI para gabarito
- `listar_provas()` - Mostra provas disponíveis
- `mostrar_ajuda()` - Exibe ajuda

**Importa**: config_provas, extrator_questoes, atualizador_gabarito

---

## 2️⃣ `config_provas.py` 📋

**O que faz**: Centraliza a configuração de todas as provas

**Classes**:
```python
@dataclass
ConfigProva(
    nome: str,              # "Polícia Civil 2025"
    codigo_prefixo: str,    # "pc2025"
    arquivo_entrada: str,   # "dataset_pc2025.txt"
    arquivo_saida: str,     # "questoes_pc2025.csv"
    descricao: str          # "Prova de Polícia Civil de 2025"
)
```

**Funções**:
- `obter_config_prova(tipo_prova: str) -> ConfigProva`
  - Obtém config de uma prova específica
  - Lança ValueError se tipo não existe

- `listar_provas_disponiveis() -> None`
  - Exibe lista de provas disponíveis

**Como adicionar nova prova**:
```python
PROVAS_DISPONIVEIS = {
    'pc2025': ConfigProva(...),    # Existente
    'pm2025': ConfigProva(         # Adicione
        nome='Polícia Militar 2025',
        codigo_prefixo='pm2025',
        arquivo_entrada='dataset_pm2025.txt',
        arquivo_saida='questoes_pm2025.csv',
        descricao='Prova PM 2025'
    ),
}
```

---

## 3️⃣ `extrator_questoes.py` 📖

**O que faz**: Extrai questões de arquivo TXT e salva em CSV

**Classes**:

### `Questao` (dataclass)
```python
Questao(
    id: str,                        # "pc2025_01_pn_31"
    codigo_prova: str,              # "pc2025_01_pn"
    numero: str,                    # "31"
    enunciado: str,                 # "João, reincidente..."
    alternativas: Dict[str, str]    # {"A": "simples...", "B": "qualificado..."}
)
```

### `ExtratorQuestoesTXT`

**Método**: `__init__(caminho_arquivo: str)`
- Inicializa com o caminho do arquivo TXT
- Lança FileNotFoundError se arquivo não existe

**Método**: `extrair() -> List[Questao]`
- Extrai todas as questões do arquivo
- Retorna lista de objetos Questao

**Método**: `para_csv(caminho_saida: str) -> None`
- Salva questões em arquivo CSV
- Formato: id, enunciado, opcao, texto_alternativa, resposta

**Métodos internos** (privados):
- `_processar_bloco(bloco: str)` - Processa um código de prova
- `_processar_questao()` - Extrai uma questão
- `_extrair_alternativas()` - Extrai alternativas A-E

**Exemplo de uso**:
```python
from extrator_questoes import ExtratorQuestoesTXT

extrator = ExtratorQuestoesTXT('src/dataset/dataset_pc2025.txt')
questoes = extrator.extrair()  # 138 questões
extrator.para_csv('src/dataset/questoes_pc2025.csv')
```

---

## 4️⃣ `atualizador_gabarito.py` ✏️

**O que faz**: Atualiza as respostas corretas no CSV

**Classe**: `AtualizadorGabarito`

**Método**: `__init__(caminho_csv: str)`
- Inicializa com arquivo CSV
- Lança FileNotFoundError se CSV não existe

**Método**: `carregar_gabarito(caminho_gabarito: str) -> None`
- Carrega gabarito de arquivo de texto
- Formato esperado:
  ```
  # Comentários com #
  pc2025_01_pn_31:C
  pc2025_01_pn_32:E
  ...
  ```
- Valida formato (ID:RESPOSTA) e resposta (A-E)

**Método**: `carregar_csv() -> None`
- Carrega o CSV em memória
- Chamado automaticamente por `atualizar()`

**Método**: `atualizar() -> Tuple[int, int]`
- Atualiza respostas: 1 = correta, 0 = errada
- Salva CSV atualizado
- Retorna (linhas_atualizadas, linhas_sem_gabarito)

**Método**: `gerar_relatorio() -> None`
- Mostra quantas questões têm gabarito
- Lista questões sem gabarito

**Exemplo de uso**:
```python
from atualizador_gabarito import AtualizadorGabarito

atualizador = AtualizadorGabarito('src/dataset/questoes_pc2025.csv')
atualizador.carregar_gabarito('gabarito_pc2025.txt')
atualizador.gerar_relatorio()
atualizado, sem_gab = atualizador.atualizar()
print(f"{atualizado} respostas atualizadas")
```

---

## 5️⃣ `gerar_gabarito_exemplo.py` 📝

**O que faz**: Gera um arquivo de exemplo de gabarito para preenchimento

**Função**: `gerar_exemplo_gabarito() -> None`
- Cria `src/dataset/gabarito_pc2025_exemplo.txt`
- Com exemplos de formato correto
- Com seções comentadas para cada disciplina

**Como usar**:
```bash
python gerar_gabarito_exemplo.py
```

Depois edite o arquivo e use:
```bash
python main.py gabarito pc2025 src/dataset/gabarito_pc2025_exemplo.txt
```

---

## 📊 Fluxos de Uso

### Fluxo 1: Extrair Sem Gabarito
```bash
python main.py extrair pc2025
✓ Cria questoes_pc2025.csv com resposta=0 para todas
```

### Fluxo 2: Extrair + Gabarito Completo
```bash
# 1. Extrair
python main.py extrair pc2025

# 2. Gerar template
python gerar_gabarito_exemplo.py

# 3. Editar gabarito_pc2025_exemplo.txt

# 4. Atualizar
python main.py gabarito pc2025 src/dataset/gabarito_pc2025_exemplo.txt
```

### Fluxo 3: Múltiplas Provas
```bash
# PC2025
python main.py extrair pc2025
python main.py gabarito pc2025 gabarito_pc2025.txt

# PM2025
python main.py extrair pm2025
python main.py gabarito pm2025 gabarito_pm2025.txt
```

---

## 🔧 Exemplo Prático Completo

```python
# script_exemplo.py - Usando os módulos diretos

from config_provas import obter_config_prova
from extrator_questoes import ExtratorQuestoesTXT
from atualizador_gabarito import AtualizadorGabarito

# 1. Obter configuração da prova
config = obter_config_prova('pc2025')
print(f"Processando: {config.descricao}")

# 2. Extrair questões
extrator = ExtratorQuestoesTXT(f'src/dataset/{config.arquivo_entrada}')
questoes = extrator.extrair()
print(f"Total: {len(questoes)} questões")

# 3. Salvar em CSV
extrator.para_csv(f'src/dataset/{config.arquivo_saida}')

# 4. Atualizar gabarito
atualizador = AtualizadorGabarito(f'src/dataset/{config.arquivo_saida}')
atualizador.carregar_gabarito('gabarito_pc2025.txt')
atualizador.gerar_relatorio()
atualizado, sem_gab = atualizador.atualizar()

print(f"\nResultado final:")
print(f"  Questões: {len(questoes)}")
print(f"  Respostas atualizadas: {atualizado}")
print(f"  Sem gabarito: {sem_gab}")
```

---

## ⚙️ Parâmetros e Configurações

### Variáveis de Ambiente (não usam, mas poderiam)
Nenhuma por enquanto - tudo é via CLI ou arquivo

### Arquivos de Configuração
- `config_provas.py` - Define PROVAS_DISPONIVEIS (editava aqui)

### Codificação
- Todos arquivos: UTF-8 com BOM
- CSV: UTF-8-sig (compatível com Excel)

---

## 📝 Convenções de Código

- **Nomes de variáveis**: snake_case
- **Classes**: PascalCase
- **Constantes**: UPPER_SNAKE_CASE
- **Funções privadas**: `_nome()`
- **Type hints**: Em todas as funções

---

## 🧪 Testes Manuais

### Teste 1: Listar
```bash
python main.py listar
✓ Deve exibir: Polícia Civil 2025 e Polícia Militar 2025
```

### Teste 2: Extrair
```bash
python main.py extrair pc2025
✓ Deve crear: src/dataset/questoes_pc2025.csv
✓ Deve haver: 138 questões, 690 linhas
```

### Teste 3: Gabarito
```bash
python gerar_gabarito_exemplo.py
python main.py gabarito pc2025 src/dataset/gabarito_pc2025_exemplo.txt
✓ Deve atualizar respostas
✓ 27 entradas carregadas do exemplo
✓ 160 respostas atualizadas (5 per questão × 27)
```

---

## 🚀 Dicas e Truques

1. **Adicionar nova prova rapidamente**
   - Edit `config_provas.py`
   - Drop arquivo TXT em `src/dataset/`
   - Execute `python main.py extrair <tipo>`

2. **Verificar questões extraídas**
   - Abra `questoes_pc2025.csv` em Excel
   - Filtre por `opcao = A` para ver enunciados únicos

3. **Corrigir gabarito depois**
   - Edite o arquivo de gabarito
   - Reexecute `python main.py gabarito`

4. **Ver questões sem gabarito**
   - O relatório mostra a lista completa
   - Adicione ao arquivo de gabarito conforme necessário

---

**Referência Completa**: Março 2026  
**Sistema**: Modularizado v2.0
