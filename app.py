from flask import Flask, render_template, request
import pdfplumber
import os
from database.pdf_repository import salvar_pdf

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_pdf():
    if "pdf" not in request.files:
        return render_template("resultado.html", texto="Nenhum arquivo enviado.")

    file = request.files["pdf"]

    if file.filename == "":
        return render_template("resultado.html", texto="Nenhum arquivo selecionado.")

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    texto_extraido = ""

    try:
        with pdfplumber.open(filepath) as pdf:
            for pagina in pdf.pages:
                texto_extraido += pagina.extract_text() or ""
                texto_extraido += "\n\n"

        # 🔹 Agora apenas chamamos a função
        salvar_pdf(file.filename, texto_extraido)

    except Exception as e:
        texto_extraido = f"Erro ao processar ou salvar: {str(e)}"

    return render_template("resultado.html", texto=texto_extraido)


if __name__ == "__main__":
    app.run(debug=True)