from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
import os

# Gera um PDF em formato de tabela, com cabeçalhos e colunas, refletindo o hemograma do exemplo

def main():
    out_dir = os.path.join(os.getcwd(), "tests", "exemplos")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "hemograma_tabela.pdf")

    c = canvas.Canvas(out_path, pagesize=A4)
    w, h = A4

    # Título
    c.setFont("Helvetica-Bold", 14)
    c.drawString(20*mm, h - 20*mm, "Hemograma com Contagem de Plaquetas")

    # Cabeçalho "Série Vermelha"
    c.setFont("Helvetica-Bold", 12)
    y = h - 35*mm
    c.drawString(20*mm, y, "Série Vermelha")
    y -= 8*mm

    # Cabeçalhos das colunas
    c.setFont("Helvetica", 10)
    c.drawString(20*mm, y, "Parâmetro")
    c.drawString(80*mm, y, "RESULTADO")
    c.drawString(130*mm, y, "INTERVALO DE REFERÊNCIA")
    y -= 7*mm

    c.setFont("Helvetica", 11)

    def row(param, resultado, referencia):
        nonlocal y
        c.drawString(20*mm, y, param)
        c.drawString(80*mm, y, resultado)
        c.drawString(130*mm, y, referencia)
        y -= 7*mm

    # Série Vermelha linhas
    row("Eritrócitos", "4,43 10^6/µL", "4,50 a 5,50 10^6/µL")
    row("Hemoglobina", "14,6 g/dL", "13,0 a 17,0 g/dL")
    row("Hematócrito", "42,6 %", "40,0 a 50,0 %")
    row("VCM", "96,2 fL", "83,0 a 101,0 fL")
    row("HCM", "33,0 pg", "27,0 a 32,0 pg")
    row("CHCM", "34,3 g/dL", "31,0 a 35,0 g/dL")
    row("RDW", "11,8 %", "11,6 a 14,0 %")

    # Separadores e notas
    y -= 6*mm
    c.setFont("Helvetica", 9)
    c.drawString(130*mm, y, "(Material:Sangue Total)")
    y -= 4*mm
    c.setFont("Helvetica", 9)
    c.drawString(20*mm, y, "(Método:Impedância / Colorimetria / Fluorescência / Avaliação Microscópica)")

    # Linha divisória
    y -= 6*mm
    c.setFont("Helvetica", 12)
    c.drawString(20*mm, y, "-"*80)
    y -= 6*mm

    # Cabeçalho "Série Branca"
    c.setFont("Helvetica-Bold", 12)
    c.drawString(20*mm, y, "Série Branca")
    y -= 8*mm

    # Cabeçalhos das colunas
    c.setFont("Helvetica", 10)
    c.drawString(20*mm, y, "Parâmetro")
    c.drawString(80*mm, y, "RESULTADO")
    c.drawString(130*mm, y, "INTERVALO DE REFERÊNCIA")
    y -= 7*mm

    c.setFont("Helvetica", 11)
    row("Leucócitos", "100 % 6.970 /µL", "100 % | 4.000 a 10.000 /µL")
    row("Neutrófilos", "50,9 % 3.548 /µL", "40,0 a 80,0 % | 1.800 a 7.800 /µL")
    row("Eosinófilos", "11,5 % 802 /µL", "1,0 a 6,0 % | 20 a 500 /µL")
    row("Basófilos", "0,5 % 35 /µL", "0,0 a 2,0 % | 20 a 100 /µL")
    row("Linfócitos", "31,8 % 2.216 /µL", "20,0 a 40,0 % | 1.000 a 3.000 /µL")
    row("Monócitos", "5,3 % 369 /µL", "2,0 a 10,0 % | 200 a 1.000 /µL")

    # Plaquetas
    y -= 4*mm
    c.setFont("Helvetica-Bold", 12)
    c.drawString(20*mm, y, "Plaquetas")
    y -= 8*mm
    c.setFont("Helvetica", 11)
    row("Contagem de plaquetas", "282.000 /µL", "150.000 a 450.000 /µL")

    c.showPage()
    c.save()

    print(f"PDF gerado em: {out_path}")

if __name__ == "__main__":
    main()