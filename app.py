# Importa a classe principal do Flask para criar a aplicação,
# render_template para renderizar arquivos HTML,
# e request para acessar dados enviados pelo usuário (como upload de arquivos)
from flask import Flask, render_template, request

# Biblioteca utilizada para abrir e extrair texto de arquivos PDF
import pdfplumber

# Biblioteca padrão do Python para manipulação de arquivos e diretórios
import os

# Importa a função responsável por salvar os dados no banco de dados
# (está separada em outro módulo para manter organização do projeto)
from database.pdf_repository import salvar_pdf


# Cria a instância principal da aplicação Flask
# __name__ informa ao Flask onde está localizado o arquivo principal
app = Flask(__name__)


# Define o nome da pasta onde arquivos poderiam ser salvos futuramente
UPLOAD_FOLDER = "uploads"

# Garante que a pasta exista.
# Se não existir, ela será criada automaticamente.
# exist_ok=True evita erro caso a pasta já exista.
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ==============================
# ROTA PRINCIPAL
# ==============================

# Define a rota raiz ("/")
# Quando o usuário acessa http://localhost:5000/
# essa função será executada.
@app.route("/")
def home():
    # Renderiza o arquivo templates/index.html
    # Essa é a página onde o usuário faz upload do PDF
    return render_template("index.html")


# ==============================
# ROTA DE UPLOAD
# ==============================

# Define a rota "/upload"
# methods=["POST"] indica que essa rota só aceita requisições do tipo POST
# (envio de formulário)
@app.route("/upload", methods=["POST"])
def upload_pdf():

    # Verifica se existe um arquivo chamado "pdf"
    # dentro dos arquivos enviados pelo formulário
    if "pdf" not in request.files:
        return render_template("resultado.html", texto="Nenhum arquivo enviado.")

    # Recupera o arquivo enviado pelo usuário
    file = request.files["pdf"]

    # Verifica se o usuário realmente selecionou um arquivo
    if file.filename == "":
        return render_template("resultado.html", texto="Nenhum arquivo selecionado.")

    # Variável que armazenará todo o texto extraído do PDF
    texto_extraido = ""

    try:
        # ==============================
        # EXTRAÇÃO DO PDF DIRETO DA MEMÓRIA
        # ==============================
        # file.stream contém o arquivo em memória (sem salvar no disco)
        # pdfplumber.open abre o PDF para leitura
        with pdfplumber.open(file.stream) as pdf:

            # Percorre todas as páginas do PDF
            for pagina in pdf.pages:

                # extract_text() extrai o texto da página
                # Caso não haja texto na página, retorna None
                # Por isso usamos "or """ para evitar erro
                texto_extraido += pagina.extract_text() or ""

                # Adiciona quebra de linha entre páginas
                texto_extraido += "\n\n"

        # ==============================
        # SALVAR ARQUIVO FISICAMENTE (OPCIONAL)
        # *************************************************************************************
        # Caso futuramente seja necessário salvar o PDF no servidor,
        # basta descomentar as linhas abaixo:

        # filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        # file.save(filepath)

        # ********************************************************************************
        
        # SALVAR TEXTO NO BANCO DE DADOS
        # ==============================
        # Chama a função importada do módulo database,
        # enviando o nome do arquivo e o texto extraído
        salvar_pdf(file.filename, texto_extraido)

    except Exception as e:
        # Caso ocorra qualquer erro durante a extração
        # ou durante o salvamento no banco,
        # a mensagem de erro será exibida na página de resultado
        texto_extraido = f"Erro ao processar ou salvar: {str(e)}"

    # Renderiza a página resultado.html
    # Passando o texto extraído como variável para o template
    return render_template("resultado.html", texto=texto_extraido)


# ==============================
# INICIALIZAÇÃO DA APLICAÇÃO
# ==============================

# Esse bloco garante que o servidor Flask só será iniciado
# se este arquivo for executado diretamente (python app.py)
# e não quando for importado como módulo em outro arquivo.
if __name__ == "__main__":

    # debug=True ativa:
    # - recarregamento automático ao salvar alterações
    # - mensagens detalhadas de erro
    # ⚠️ Nunca usar debug=True em produção
    app.run(debug=True)