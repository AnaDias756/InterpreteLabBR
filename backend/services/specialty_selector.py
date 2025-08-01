from collections import Counter


def select_specialties(analyzed_findings, top_n=3):
    """
    Soma os scores de severidade para cada especialidade e retorna um ranking.
    """
    if not analyzed_findings:
        return []

    score = Counter()
    for finding in analyzed_findings:
        # A severidade já é um número (ex: 1, 2, 3) vindo do analyzer
        # O split() permite que o CSV tenha múltiplas especialidades (ex: "Hematologia, Clínico")
        especialidades = [esp.strip() for esp in finding["especialidade"].split(',')]
        for esp in especialidades:
            score[esp] += finding["severidade"]

    # Retorna apenas as especialidades com score maior que 0
    ranked = [esp for esp, scr in score.most_common(top_n) if scr > 0]
    return ranked