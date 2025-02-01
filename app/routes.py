from flask import Blueprint, render_template, request, send_file, redirect, url_for, flash
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import textwrap
from io import BytesIO
from datetime import datetime

# Cria um blueprint para as rotas principais
main_bp = Blueprint("main", __name__)

@main_bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Obter dados do formulário
        data = request.form.get("data")
        atividade = request.form.get("atividade").strip()

        # Validar entrada
        if not atividade:
            flash("Por favor, insira uma atividade.", "error")
            return redirect(url_for("main.index"))

        # Gerar o PDF
        try:
            # Criar um buffer de memória para o PDF
            buffer = BytesIO()

            # Criar o PDF
            c = canvas.Canvas(buffer, pagesize=A4)
            largura, altura = A4
            margem_esquerda = 72  # 1 polegada
            margem_superior = 72  # 1 polegada

            # Configurar título
            c.setFont("Helvetica-Bold", 14)
            c.drawString(margem_esquerda, altura - margem_superior, "Relatório de Atividades")

            # Configurar corpo do texto
            c.setFont("Helvetica", 12)
            texto_padrao = f"Acolhimento/ Café da manhã/ Lanche/ Roda de conversa sobre {atividade} na data {data}."
            largura_texto = largura - 2 * margem_esquerda
            linhas = textwrap.wrap(texto_padrao, width=80)

            y = altura - margem_superior - 30  # Posição inicial
            for linha in linhas:
                if y < margem_superior:  # Nova página se o texto ultrapassar
                    c.showPage()
                    c.setFont("Helvetica", 12)
                    y = altura - margem_superior
                c.drawString(margem_esquerda, y, linha)
                y -= 15  # Espaçamento entre linhas

            c.showPage()
            c.save()

            # Retornar o PDF para download
            buffer.seek(0)
            return send_file(
                buffer,
                as_attachment=True,
                download_name=f"relatorio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mimetype="application/pdf",
            )
        except Exception as e:
            flash(f"Erro ao gerar o relatório: {e}", "error")
            return redirect(url_for("main.index"))

    return render_template("index.html")