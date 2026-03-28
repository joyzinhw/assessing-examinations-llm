# 📂 Estrutura de Arquivos do Projeto

## ✅ Arquivos ATUAIS (Usar Estes)

### Scripts Principais (use estes!)

```
✅ main.py                      ⭐ PRINCIPAL - use este
✅ config_provas.py             📋 Define provas
✅ extrator_questoes.py         📖 Extrai questões
✅ atualizador_gabarito.py      ✏️ Atualiza gabarito
✅ gerar_gabarito_exemplo.py    📝 Gera template
```

### Documentação

```
✅ README_SISTEMA.md            📘 Guia completo
✅ RESUMO_REFATORACAO.md        🔄 O que mudou
✅ REFERENCIA_SCRIPTS.md        📚 Referência de funções
✅ ESTRUTURA_ARQUIVOS.md        📂 Este arquivo
```

---

## ❌ Arquivos ANTIGOS (Deletar Estes)

Estes arquivos foram substituídos pela nova arquitetura:

```
❌ converter.py                 - Substituído por extrator_questoes.py
❌ corrigir_csv.py              - Não mais necessário (UTF-8-sig está integrado)
❌ extrair_final.py             - Substituído por extrator_questoes.py
❌ extrair_questoes.py          - Versão antiga, versão nova é extrator_questoes.py
❌ atualizar_gabarito.py        - Versão antiga, versão nova é atualizador_gabarito.py
❌ json_to_csv.py               - Não necessário (JSON estava vazio)
❌ README_QUESTOES.md           - Substituído por README_SISTEMA.md
```

### Limpeza Recomendada

```bash
# Deletar arquivos antigos
del converter.py
del corrigir_csv.py
del extrair_final.py
del extrair_questoes.py
del atualizar_gabarito.py
del json_to_csv.py
del README_QUESTOES.md
```

---

## 📁 Estrutura de Pastas

```
assessing-examinations-llm/
│
├── 📚 SCRIPTS (Use estes!)
│   ├── main.py                  ⭐ Inicie aqui
│   ├── config_provas.py          
│   ├── extrator_questoes.py      
│   ├── atualizador_gabarito.py   
│   └── gerar_gabarito_exemplo.py 
│
├── 📖 DOCUMENTAÇÃO
│   ├── README_SISTEMA.md         
│   ├── RESUMO_REFATORACAO.md     
│   ├── REFERENCIA_SCRIPTS.md     
│   └── ESTRUTURA_ARQUIVOS.md    (este)
│
├── 📂 src/
│   ├── dataset/
│   │   ├── dataset_pc2025.txt           (entrada)
│   │   ├── questoes_pc2025.csv          (saída)
│   │   ├── gabarito_pc2025_exemplo.txt  (template)
│   │   ├── gabarito_pc2025.txt          (você preenche)
│   │   └── dataset_pm2025.txt           (opcional)
│   │
│   ├── json.py               (antigo - para referência)
│   ├── main.py               (antigo - para referência)
│   └── tratamentoquestao.py  (antigo - para referência)
│
├── 📚 llm/
│   └── (modelos de LLM - não modificar)
│
├── 📜 LICENSE
└── 📝 Outros arquivos do projeto
```

---

## 🎯 Workflow Recomendado

### 1º Passo: Limpar Arquivos Antigos

```bash
cd C:\Users\Pedro\OneDrive\Área de Trabalho\assessing-examinations-llm

# Deletar old scripts
del converter.py
del corrigir_csv.py
del extrair_final.py
del extrair_questoes.py
del atualizar_gabarito.py
del json_to_csv.py
del README_QUESTOES.md

# Deletar cache
rmdir /s __pycache__
```

### 2º Passo: Verificar Estrutura

```bash
# Arquivos Python devem ser:
# ✅ main.py
# ✅ config_provas.py
# ✅ extrator_questoes.py
# ✅ atualizador_gabarito.py
# ✅ gerar_gabarito_exemplo.py

# Documentação deve ser:
# ✅ README_SISTEMA.md
# ✅ RESUMO_REFATORACAO.md
# ✅ REFERENCIA_SCRIPTS.md
# ✅ ESTRUTURA_ARQUIVOS.md
```

### 3º Passo: Usar o Sistema

```bash
# Listar provas
python main.py listar

# Extrair questões
python main.py extrair pc2025

# Atualizar gabarito
python main.py gabarito pc2025 src/dataset/gabarito_pc2025.txt
```

---

## 📊 Tabela de Arquivos e Propósito

| Arquivo | Tipo | Propósito | Status |
|---------|------|----------|--------|
| main.py | Script | Orquestra o sistema (CLI) | ✅ Usar |
| config_provas.py | Módulo | Define provas disponíveis | ✅ Usar |
| extrator_questoes.py | Módulo | Extrai TXT → CSV | ✅ Usar |
| atualizador_gabarito.py | Módulo | Atualiza CSV | ✅ Usar |
| gerar_gabarito_exemplo.py | Script | Gera template | ✅ Usar |
| README_SISTEMA.md | Doc | Guia de uso completo | ✅ Ler |
| RESUMO_REFATORACAO.md | Doc | O que mudou | ✅ Ler |
| REFERENCIA_SCRIPTS.md | Doc | Referência de funções | ✅ Consultar |
| ESTRUTURA_ARQUIVOS.md | Doc | Este arquivo | ✅ Você está aqui |
| --- | --- | --- | --- |
| converter.py | Script | Converter JSON (antigo) | ❌ Deletar |
| corrigir_csv.py | Script | Codificação (antigo) | ❌ Deletar |
| extrair_final.py | Script | Extração (versão antiga) | ❌ Deletar |
| extrair_questoes.py | Script | Extração (versão antiga) | ❌ Deletar |
| atualizar_gabarito.py | Script | Gabarito (versão antiga) | ❌ Deletar |
| json_to_csv.py | Script | JSON (antigo) | ❌ Deletar |
| README_QUESTOES.md | Doc | Guia antigo | ❌ Deletar |

---

## 🚀 Próximas Etapas

### Imediato (Faça Agora)

1. ✅ **Remova arquivos antigos**
   ```bash
   del converter.py corrigir_csv.py extrair_final.py
   ```

2. ✅ **Limpe cache**
   ```bash
   rmdir /s __pycache__
   ```

3. ✅ **Leia a documentação**
   - README_SISTEMA.md (começar)
   - REFERENCIA_SCRIPTS.md (consultar funções)

### Uso do Sistema

1. **Extrair PC2025**
   ```bash
   python main.py extrair pc2025
   ```

2. **Atualizar Gabarito**
   ```bash
   python gerar_gabarito_exemplo.py
   # Edite src/dataset/gabarito_pc2025.exemplo.txt
   python main.py gabarito pc2025 src/dataset/gabarito_pc2025_exemplo.txt
   ```

3. **Adicionar PM2025**
   - Edit config_provas.py
   - Coloque dataset_pm2025.txt em src/dataset/
   - Execute `python main.py extrair pm2025`

---

## 🎓 Para Aprender o Sistema

1. **Leia primeiro**: RESUMO_REFATORACAO.md
2. **Use depois**: README_SISTEMA.md
3. **Consulte**: REFERENCIA_SCRIPTS.md
4. **Explore código**: Comece por config_provas.py (mais simples)

---

## ⚙️ Manutenção

### Antes de Fazer Mudanças

1. Leia REFERENCIA_SCRIPTS.md
2. Entenda a arquitetura em RESUMO_REFATORACAO.md
3. Se adicionar nova prova, edit config_provas.py

### Se der Problema

1. Delete __pycache__ (cache pode causar problemas)
2. Verifique se todos os imports estão corretos
3. Consulte REFERENCIA_SCRIPTS.md para funções e parâmetros

### Boas Práticas

✅ Use sempre `python main.py` (não scripts individuais)  
✅ Edit `config_provas.py` para adicionar provas  
✅ Mantenha arquivos TXT em `src/dataset/`  
✅ Use UTF-8 para todos os arquivos  
✅ Siga a convenção de naming  

---

## 🔍 Checklist de Setup

- [ ] Python 3.8+ instalado
- [ ] Pasta `src/dataset/` existe
- [ ] Arquivo `dataset_pc2025.txt` em `src/dataset/`
- [ ] Executável `python main.py listar` funciona
- [ ] Arquivos antigos deletados (opcional, mas recomendado)
- [ ] __pycache__ deletado (opcional, mas recomendado)

---

## 📞 Suporte Rápido

| Problema | Solução |
|----------|---------|
| "Arquivo não encontrado" | Coloque arquivo TXT em src/dataset/ |
| "ModuleNotFoundError" | Delete __pycache__ e tente novamente |
| Questões não extraídas | Confira formato do TXT |
| Gabarito não funcionando | Confira formato do arquivo (ID:RESPOSTA) |
| Provas não listadas | Edit config_provas.py |

---

**Estrutura de Arquivos**: Março 2026  
**Sistema**: Refatorado v2.0  
**Status**: ✅ Pronto para uso
