# LLM Prompt Benchmark & Evaluation 🚀

Script em Python que compara estratégias de *prompting* (**prompt direto** vs. **few-shot**) usando a API do Google Gemini, executa os experimentos de forma automatizada e organiza os resultados em uma planilha Excel para análise.

O objetivo é simular, em pequena escala, um fluxo real de experimentação com LLMs: definir um cenário, rodar variações de prompt, coletar métricas e comparar os resultados.

---

## 🎯 O que o projeto faz

- Executa prompts automaticamente via API do Gemini
- Compara duas técnicas de prompting **de forma controlada** (mesma instrução, só os exemplos mudam)
- Repete cada experimento várias vezes para reduzir o efeito da variação das respostas
- Registra métricas por execução: caracteres, palavras, latência e erros
- Gera um relatório em Excel com os dados completos e um resumo por técnica

---

## 🧪 Desenho do experimento

| Item | Configuração |
|------|--------------|
| Perguntas | 3 (negócio, riscos de IA generativa, observabilidade em pagamentos) |
| Técnicas | Prompt Direto · Few-Shot (2 exemplos) |
| Execuções por prompt | 3 (18 chamadas no total) |
| Temperatura | 0.2 |
| Modelo | Configurável via `GEMINI_MODEL` (padrão: `gemini-2.5-flash`) |

**Prompt Direto:** instrução + pergunta.
**Few-Shot:** a mesma instrução + 2 exemplos de pergunta/resposta + pergunta.

Os exemplos do few-shot não repetem as perguntas do teste, para evitar viés.

---

## 📊 Resultados

O script gera o arquivo `benchmark_llm_resultados.xlsx` com duas abas:

- **Resultados:** uma linha por execução, com pergunta, técnica, prompt enviado, resposta, caracteres, palavras, latência e erro
- **Resumo:** médias por técnica, número de execuções válidas e número de execuções com erro


---

## 🛠️ Tecnologias

- **Python**
- **Google GenAI SDK** (`google-genai`)
- **Pandas**
- **Openpyxl**
- **Python-dotenv**

---

## 📁 Estrutura do projeto

```text
llm-prompt-evaluation/
│
├── benchmark.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

O arquivo `benchmark_llm_resultados.xlsx` é gerado ao executar o script.

---

## ⚙️ Como executar

### 1. Clonar o repositório

```bash
git clone https://github.com/GiovanniCabralO/llm-prompt-evaluation.git
cd llm-prompt-evaluation
```

### 2. Instalar as dependências

```bash
python -m pip install -r requirements.txt
```

### 3. Configurar a chave da API

Copie `.env.example` para `.env` e preencha:

```text
GEMINI_API_KEY=sua_chave_aqui
# Opcional: escolha outro modelo caso o padrão esteja indisponível
# GEMINI_MODEL=gemini-2.5-flash
```

A chave pode ser gerada no [Google AI Studio](https://aistudio.google.com/apikey).

### 4. Executar o benchmark

```bash
python benchmark.py
```

---

## ⚠️ Limitações

- A amostra é pequena (3 perguntas × 3 execuções), então os resultados serão ilustrativos, não estatisticamente conclusivos.
- As métricas atuais medem **forma** (tamanho e latência), não **qualidade** do conteúdo. A avaliação da qualidade das respostas é manual.

## 🔭 Próximos passos

- Executar o benchmark e publicar os resultados e a análise
- Incluir avaliação automática de qualidade (por exemplo, *LLM-as-a-judge* com critérios definidos)
- Ampliar o conjunto de perguntas e comparar mais de um modelo
- Testar outras técnicas, como *chain-of-thought* e instruções de formato

---

## 👨‍💻 Autor

**Giovanni Cabral**
[LinkedIn](https://www.linkedin.com/in/giovannicabraldeoliveira/) · [GitHub](https://github.com/GiovanniCabralO)