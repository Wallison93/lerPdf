from database.connection import conectar

def salvar_pdf(nome_arquivo, texto):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        INSERT INTO testepython (nome_arquivo, texto)
        VALUES (%s, %s)
    """

    cursor.execute(sql, (nome_arquivo, texto))
    conexao.commit()

    cursor.close()
    conexao.close()