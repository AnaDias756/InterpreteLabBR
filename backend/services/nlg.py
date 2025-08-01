import requests

def build_briefing(findings: list[dict], specialties: list[str]) -> str:
    resumo = ", ".join(f"{f['analito']}: {f['sev']}" for f in findings)
    prompt = (
        "Você é um assistente de saúde. Meu exame apresentou os seguintes achados: "
        + resumo + ". "
        + f"Vou consultar um especialista em {', '.join(specialties)}. "
        "O que posso relatar ao médico?"
    )

    response = requests.post("http://localhost:11434/api/generate", json={
        "model": "phi",  # modelo leve compatível com máquinas com menos RAM
        "prompt": prompt,
        "stream": False
    })

    data = response.json()
    if "response" not in data:
        raise ValueError(f"Erro ao gerar resposta: {data}")

    return data["response"]