# 🎯 Sistema Refatorado - Resumo das Mudanças

## ✅ O Que Mudou

O código foi completamente refatorado para ser:

1. **🏗️ Modularizado**
   - Separado em 4 módulos independentes e reutilizáveis
   - Cada módulo tem responsabilidade única

2. **📚 Documentado**
   - Docstrings em todas as classes e funções
   - Exemplos de uso
   - Comentários explicativos

3. **🔧 Extensível**
   - Fácil adicionar novos tipos de provas em `config_provas.py`
   - Suporta múltiplas provas simultaneamente (pc2025, pm2025, etc)

4. **💪 Robusto**
   - Tratamento de erros
   - Validações de entrada
   - Relatórios detalhados

5. **👤 User-Friendly**
   - Interface CLI clara em `main.py`
   - Mensagens de erro úteis
   - Ajuda integrada

## 📁 Arquivos Criados/Modificados

### Módulos Principais

| Arquivo | Responsabilidade |
|---------|-----------------|
| `config_provas.py` | Define quais provas estão disponíveis |
| `extrator_questoes.py` | Extrai questões de TXT → CSV |
| `atualizador_gabarito.py` | Atualiza respostas corretas no CSV |
| `main.py` | Interface CLI que orquestra tudo |

### Arquivos de Suporte

| Arquivo | Responsabilidade |
|---------|-----------------|
| `gerar_gabarito_exemplo.py` | Gera arquivo de exemplo para preenchimento |
| `README_SISTEMA.md` | Documentação completa do sistema |

## 🚀 Como Usar

### Passo 1: Listar Provas Disponíveis

```bash
python main.py listar
```

### Passo 2: Extrair Questões

```bash
# Extrai dataset_pc2025.txt → questoes_pc2025.csv
python main.py extrair pc2025

# Ou extrair outra prova
python main.py extrair pm2025
```

### Passo 3: Atualizar Gabarito (Opcional)

```bash
# Cria arquivo de exemplo
python gerar_gabarito_exemplo.py

# Edite: src/dataset/gabarito_pc2025.txt

# Atualizar
python main.py gabarito pc2025 src/dataset/gabarito_pc2025.txt
```

## 🔄 Fluxo de Dados

```
dataset_pc2025.txt (TXT)
        ↓
   ExtratorQuestoesTXT
        ↓
questoes_pc2025.csv (CSV)
        ↓
   AtualizadorGabarito
        ↓
questoes_pc2025.csv (atualizado com respostas)
```

## 📋 Formato de Gabarito

Arquivo simples de texto:

```
# Comentários são ignorados
pc2025_01_pn_31:C
pc2025_01_pn_32:E
pc2025_01_pn_33:B
...
```

**Formato**: `ID_QUESTAO:RESPOSTA` (resposta = A, B, C, D ou E)

## ➕ Adicionar Nova Prova (PM2025)

### 1. Editar `config_provas.py`:

```python
PROVAS_DISPONIVEIS = {
    'pc2025': ConfigProva(...),  # Já existe
    'pm2025': ConfigProva(       # Novo
        nome='Polícia Militar 2025',
        codigo_prefixo='pm2025',
        arquivo_entrada='dataset_pm2025.txt',
        arquivo_saida='questoes_pm2025.csv',
        descricao='Prova de Polícia Militar de 2025'
    ),
}
```

### 2. Colocar arquivo em `src/dataset/dataset_pm2025.txt`

### 3. Usar normalmente:

```bash
python main.py extrair pm2025
python main.py gabarito pm2025 gabarito_pm2025.txt
```

## 🔍 Arquitetura Detalhada

### `config_provas.py`
- **Classe**: `ConfigProva` (dataclass)
- **Função**: `obter_config_prova(tipo)` → retorna config
- **Função**: `listar_provas_disponiveis()` → exibe todas

### `extrator_questoes.py`
- **Classe**: `Questao` (dataclass) - representa uma questão
- **Classe**: `ExtratorQuestoesTXT` - processa arquivo TXT
  - `extrair()` - extrai todas as questões
  - `para_csv()` - salva em CSV

### `atualizador_gabarito.py`
- **Classe**: `AtualizadorGabarito` - atualiza CSV
  - `carregar_gabarito()` - lê arquivo de gabarito
  - `atualizar()` - marca respostas corretas
  - `gerar_relatorio()` - mostra estatísticas

### `main.py`
- **Função**: `extrair_questoes()` - CLI para extração
- **Função**: `atualizar_gabarito()` - CLI para atualização
- **Função**: `listar_provas()` - mostra provas disponíveis
- **Função**: `main()` - orquestra tudo

## 💡 Exemplos de Uso Avançado

### Extrair e atualizar tudo de uma vez

```bash
# 1. Extrair
python main.py extrair pc2025

# 2. Gerar template
python gerar_gabarito_exemplo.py

# 3. Editar gabarito_pc2025_exemplo.txt com as respostas

# 4. Atualizar
python main.py gabarito pc2025 src/dataset/gabarito_pc2025_exemplo.txt
```

### Trabalhar com múltiplas provas

```bash
# Processar PC2025
python main.py extrair pc2025
python main.py gabarito pc2025 gabarito_pc2025.txt

# Processar PM2025
python main.py extrair pm2025
python main.py gabarito pm2025 gabarito_pm2025.txt
```

### Atualizar sem gabarito

Basta não executar a etapa de gabarito. O CSV terá `resposta = 0` para todas as alternativas.

## 🎓 Estrutura de Aprendizado

Se você quer entender o código:

1. **Comece por**: `config_provas.py` (mais simples)
2. **Depois**: `extrator_questoes.py` (lógica de parsing)
3. **Depois**: `atualizador_gabarito.py` (manipulação de CSV)
4. **Finalize**: `main.py` (orquestração)

## 📊 Resultado Esperado

### Após `python main.py extrair pc2025`:

```
✨ Extração concluída com sucesso!
✓ 138 questões extraídas
✓ 690 linhas no CSV (5 alternativas × 138 questões)
```

### Após `python main.py gabarito pc2025 gabarito.txt`:

```
✓ 28 entradas carregadas do gabarito
✓ 160 respostas atualizadas
⚠️  530 linhas sem gabarito (esperado se não preencheu tudo)
```

## 🔐 Qualidades do Código

✅ **DRY** (Don't Repeat Yourself) - Sem duplicação  
✅ **SOLID** - Single Responsibility Principle aplicado  
✅ **Type Hints** - Todas as funções tipadas  
✅ **Docstrings** - Bem documentado  
✅ **Error Handling** - Trata erros graciosamente  
✅ **Testável** - Fácil de testar unitariamente  

## 🚫 Evitar Erros Comuns

❌ Não: Editar `main.py` para adicionar novas provas  
✅ Sim: Editar `config_provas.py` e adicionar ConfigProva  

❌ Não: Modificar o formato de entrada esperado  
✅ Sim: Manter a estrutura "Código: " e números de questão  

❌ Não: Editar o CSV manualmente e depois rodar atualizador  
✅ Sim: Usar o atualizador ou editar manualmente, não fazer ambos  

## 📞 Próximas Melhorias Possíveis

- [ ] Validação de integridade de dados
- [ ] Suporte a formatos diferentes de entrada
- [ ] Cache de questões extraídas
- [ ] Testes unitários
- [ ] Interface GUI (opcional)
- [ ] API REST (opcional)

---

**Sistema Refatorado**: 28 de Março de 2026  
**Versão**: 2.0 (Modularizado)  
**Status**: ✅ Pronto para uso
