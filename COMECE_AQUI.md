# 🚀 COMECE AQUI

## ⚡ Início Rápido (2 minutos)

### 1. Testar se tudo funciona
```bash
python teste_rapido.py
```
✅ Deve exibir "SISTEMA ESTÁ OK"

### 2. Ver provas disponíveis
```bash
python main.py listar
```
✅ Deve listar: Polícia Civil 2025 e Polícia Militar 2025

### 3. Extrair questões
```bash
python main.py extrair pc2025
```
✅ Cria arquivo: `src/dataset/questoes_pc2025.csv`
- 138 questões
- 690 linhas (5 alternativas × questão)

### 4. Pronto! 🎉
CSV está em `src/dataset/questoes_pc2025.csv`

---

## 📚 Arquivos de Documentação

Leia na seguinte ordem:

1. **SUMARIO_EXECUTIVO.md** (5 min)
   - O que foi feito
   - Como funciona

2. **README_SISTEMA.md** (10 min)
   - Guia completo de uso
   - Como adicionar nova prova

3. **REFERENCIA_SCRIPTS.md** (consulta)
   - Referência de funções
   - Exemplos de código

4. **ESTRUTURA_ARQUIVOS.md** (manutenção)
   - Quais arquivos deletar
   - Como organizar

---

## 📋 Comandos Principais

### Listar provas
```bash
python main.py listar
```

### Extrair questões
```bash
python main.py extrair pc2025           # Polícia Civil 2025
python main.py extrair pm2025           # Polícia Militar 2025
```

### Gerar template de gabarito
```bash
python gerar_gabarito_exemplo.py
```
Cria: `src/dataset/gabarito_pc2025_exemplo.txt`

### Atualizar gabarito
```bash
python main.py gabarito pc2025 src/dataset/gabarito_pc2025.txt
```

### Ver ajuda
```bash
python main.py ajuda
```

---

## 🎯 Caso de Uso: Extrair e Usar Questões

### Passo 1: Extrair
```bash
python main.py extrair pc2025
```

### Passo 2: Abrir CSV
- Arquivo: `src/dataset/questoes_pc2025.csv`
- Abra em Excel ou LibreOffice
- 138 questões, 690 linhas

### Passo 3: Usar para
- ✅ Estudar questões
- ✅ Testar respostas de LLM
- ✅ Análise de erros
- ✅ Treino automático

---

## ➕ Caso de Uso: Adicionar PM2025

### Passo 1: Edit `config_provas.py`
Adicione em `PROVAS_DISPONIVEIS`:
```python
'pm2025': ConfigProva(
    nome='Polícia Militar 2025',
    codigo_prefixo='pm2025',
    arquivo_entrada='dataset_pm2025.txt',
    arquivo_saida='questoes_pm2025.csv',
    descricao='Prova de Polícia Militar de 2025'
),
```

### Passo 2: Coloque arquivo
```
src/dataset/dataset_pm2025.txt
```

### Passo 3: Use como PC2025
```bash
python main.py extrair pm2025
python main.py gabarito pm2025 gabarito_pm2025.txt
```

---

## 🔧 Estrutura do Projeto

```
src/dataset/
├── dataset_pc2025.txt           ← Seu arquivo (entrada)
├── questoes_pc2025.csv          ← Gerado automaticamente
└── gabarito_pc2025.txt          ← Você preenche (opcional)
```

### Formato do Gabarito
```
# Arquivo simples de texto
pc2025_01_pn_31:C
pc2025_01_pn_32:E
pc2025_01_pn_33:B
...
```

---

## ✅ Checklist de Setup

- [ ] Executar `python teste_rapido.py` ✅
- [ ] Ver `python main.py listar` ✅
- [ ] Extrair PC2025 com `python main.py extrair pc2025` ✅
- [ ] CSV criado em `src/dataset/questoes_pc2025.csv` ✅
- [ ] Ler SUMARIO_EXECUTIVO.md
- [ ] Ler README_SISTEMA.md

---

## 🚀 Próximos Passos

### Se quer apenas extrair
1. ✅ Já está pronto!
2. Abra `src/dataset/questoes_pc2025.csv` em Excel

### Se quer adicionar gabarito
1. ✅ Execute `python gerar_gabarito_exemplo.py`
2. Edite `src/dataset/gabarito_pc2025_exemplo.txt`
3. Execute `python main.py gabarito pc2025 ...`

### Se quer adicionar PM2025
1. Edit `config_provas.py` (2 linhas)
2. Coloque `dataset_pm2025.txt` em `src/dataset/`
3. Execute `python main.py extrair pm2025`

### Se quer entender o código
1. Leia RESUMO_REFATORACAO.md
2. Veja config_provas.py (mais simples)
3. Explore extrator_questoes.py
4. Consulte REFERENCIA_SCRIPTS.md

---

## ❓ Dúvidas Frequentes

### P: Consigo usar o CSV em Excel?
**R:** Sim! Abra diretamente: `src/dataset/questoes_pc2025.csv`

### P: Como adicionar uma nova prova?
**R:** Edit `config_provas.py` (adicione 10 linhas) + coloque arquivo TXT

### P: O gabarito é obrigatório?
**R:** Não! CSV trabalha com resposta=0 para todas se quiser

### P: Posso editar manualmente o CSV?
**R:** Sim, mas não execute atualizador depois disso

### P: Funciona com Python 3.8+?
**R:** Sim! Testado em Python 3.13

---

## 📞 Suporte Rápido

| Problema | Solução |
|----------|---------|
| "Arquivo não encontrado" | Coloque arquivo TXT em src/dataset/ |
| Teste falha | Delete __pycache__ e tente novamente |
| CSV vazio | Confira formato do TXT |
| Provas não listadas | Edit config_provas.py PROVAS_DISPONIVEIS |

---

## 📚 Mapa de Documentação

```
Você está aqui
     ↓
COMECE_AQUI.md
     ↓
SUMARIO_EXECUTIVO.md (Visão geral)
     ↓
README_SISTEMA.md (Guia completo)
     ↓
REFERENCIA_SCRIPTS.md (Referência técnica)
     ↓
ESTRUTURA_ARQUIVOS.md (Manutenção)
```

---

## 🎓 O Sistema

```
┌─────────────────────────────┐
│   main.py (CLI)             │ ← Execute aqui
└────────────┬────────────────┘
             │
        ┌────┴────────────────┐
        ↓                     ↓
   Config.py          Extrator.py
   (Provas)           (TXT → CSV)
        │                     │
        └────────────┬────────┘
                     ↓
            dataset_pc2025.txt  ← Seu arquivo
                     ↓
            questoes_pc2025.csv  ← Resultado
```

---

## ✨ Características

- ✅ Modularizado (fácil de manter)
- ✅ Extensível (adicione provas facilmente)
- ✅ Documentado (código auto-explicativo)
- ✅ Testado (teste_rapido.py)
- ✅ Robusto (tratamento de erros)

---

## 🎉 Você está 100% pronto!

Comece com:
```bash
python teste_rapido.py
```

Depois use:
```bash
python main.py extrair pc2025
```

Pronto! 🚀

---

**Versão**: 2.0 (Modularizado)  
**Status**: ✅ Pronto para Produção  
**Data**: Março 28, 2026
