# Importa a função responsável por criar a conexão com o banco de dados.
# Essa função está definida no arquivo connection.py dentro da pasta database.
from database.connection import conectar


# Função responsável por salvar no banco de dados
# o nome do arquivo e o texto extraído do PDF.
def salvar_pdf(nome_arquivo, texto):

    # ==============================
    # ABERTURA DA CONEXÃO
    # ==============================
    # Chama a função conectar() que retorna uma conexão ativa com o MySQL.
    # Aqui é estabelecida a comunicação com o banco.
    conexao = conectar()

    # Cria um cursor.
    # O cursor é o objeto responsável por executar comandos SQL.
    cursor = conexao.cursor()


    # ==============================
    # COMANDO SQL
    # ==============================
    # Define a instrução SQL que será executada.
    # Estamos inserindo dados na tabela "testepython".
    #
    # (%s, %s) são placeholders (parâmetros preparados).
    # Isso evita SQL Injection e melhora a segurança.
    sql = """
        INSERT INTO testepython (nome_arquivo, texto)
        VALUES (%s, %s)
    """


    # ==============================
    # EXECUÇÃO DO INSERT
    # ==============================
    # Executa o comando SQL passando os valores
    # que substituirão os %s definidos na query.
    #
    # A ordem dos valores deve corresponder
    # à ordem das colunas no INSERT.
    cursor.execute(sql, (nome_arquivo, texto))


    # ==============================
    # CONFIRMAÇÃO DA TRANSAÇÃO
    # ==============================
    # O commit é necessário para confirmar a alteração no banco.
    # Sem o commit, o INSERT não é efetivamente salvo.
    conexao.commit()


    # ==============================
    # ENCERRAMENTO
    # ==============================
    # Fecha o cursor para liberar recursos.
    cursor.close()

    # Fecha a conexão com o banco de dados.
    # Isso evita conexões abertas desnecessariamente
    # e melhora a performance da aplicação.
    conexao.close()