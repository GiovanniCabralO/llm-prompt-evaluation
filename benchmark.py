import os
import time

import pandas as pd
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Configuração
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODELO = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
EXECUCOES_POR_PROMPT = 3
TEMPERATURA = 0.2

client = genai.Client(api_key=API_KEY)

# Cenário do benchmark
PERGUNTAS = [
    "Como a inteligência artificial gera valor para o negócio?",
    "Quais os principais riscos de adotar IA generativa em uma empresa?",
    "Por que a observabilidade é importante em sistemas de pagamento?",
]

# Mesma instrução nas duas técnicas: só os exemplos mudam.
INSTRUCAO = (
    "Você é um consultor especialista em tecnologia. "
    "Responda de forma profissional em no máximo 3 frases."
)

# Exemplos do few-shot (não repetem as perguntas do teste)
EXEMPLOS = [
    (
        "O que é Cloud Computing?",
        "É a entrega de serviços de computação pela internet, como "
        "servidores e armazenamento, permitindo inovação rápida e "
        "recursos flexíveis sob demanda.",
    ),
    (
        "Para que serve uma API?",
        "Uma API define como sistemas diferentes se comunicam, permitindo "
        "integrar serviços e reaproveitar funcionalidades sem expor "
        "detalhes internos.",
    ),
]


def montar_prompt_direto(pergunta):
    return f"{INSTRUCAO}\n\nPergunta: {pergunta}\nResposta:"


def montar_prompt_few_shot(pergunta):
    exemplos = "\n\n".join(
        f"Pergunta: {p}\nResposta: {r}" for p, r in EXEMPLOS
    )
    return f"{INSTRUCAO}\n\n{exemplos}\n\nPergunta: {pergunta}\nResposta:"


TECNICAS = {
    "Prompt Direto": montar_prompt_direto,
    "Few-Shot (2 exemplos)": montar_prompt_few_shot,
}


# Execução
def executar_prompt(prompt):
    """Chama a API e devolve (texto, erro, latência em segundos)."""
    inicio = time.perf_counter()
    try:
        resposta = client.models.generate_content(
            model=MODELO,
            contents=prompt,
            config=types.GenerateContentConfig(temperature=TEMPERATURA),
        )
        texto = resposta.text or ""
        erro = ""
    except Exception as e:
        texto = ""
        erro = str(e)
    latencia = time.perf_counter() - inicio
    return texto, erro, latencia


def main():
    if not API_KEY:
        raise SystemExit("GEMINI_API_KEY não encontrada. Verifique o .env.")

    print(f"Modelo: {MODELO} | Execuções por prompt: {EXECUCOES_POR_PROMPT}\n")

    linhas = []
    for pergunta in PERGUNTAS:
        for tecnica, montar in TECNICAS.items():
            prompt = montar(pergunta)
            for n in range(1, EXECUCOES_POR_PROMPT + 1):
                texto, erro, latencia = executar_prompt(prompt)
                linhas.append(
                    {
                        "Pergunta": pergunta,
                        "Técnica": tecnica,
                        "Execução": n,
                        "Prompt Enviado": prompt,
                        "Resposta da LLM": texto,
                        "Caracteres": len(texto),
                        "Palavras": len(texto.split()),
                        "Latência (s)": round(latencia, 2),
                        "Erro": erro,
                    }
                )
                status = "ERRO" if erro else "ok"
                print(f"[{status}] {tecnica} | exec {n} | {pergunta[:40]}...")

    df = pd.DataFrame(linhas)

    # Resumo por técnica (ignora execuções com erro)
    validos = df[df["Erro"] == ""]
    resumo = (
        validos.groupby("Técnica")[["Caracteres", "Palavras", "Latência (s)"]]
        .mean()
        .round(2)
        .reset_index()
    )
    resumo["Execuções válidas"] = (
        validos.groupby("Técnica").size().values if len(validos) else 0
    )
    resumo["Execuções com erro"] = (
        df[df["Erro"] != ""].groupby("Técnica").size().reindex(
            resumo["Técnica"], fill_value=0
        ).values
    )

    arquivo = "benchmark_llm_resultados.xlsx"
    with pd.ExcelWriter(arquivo) as writer:
        df.to_excel(writer, sheet_name="Resultados", index=False)
        resumo.to_excel(writer, sheet_name="Resumo", index=False)

    print("\nResumo por técnica:")
    print(resumo.to_string(index=False))
    print(f"\nResultados salvos em: {arquivo}")


if __name__ == "__main__":
    main()