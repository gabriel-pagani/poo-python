from pyodbc import connect, Error
from os import getenv
from dotenv import load_dotenv
import logging


load_dotenv()

# Variável global para guardar a conexão
_connection = None


def get_connection():
    """Retorna uma conexão com o banco de dados, criando-a se necessário."""
    global _connection
    if _connection is None or _connection.closed:
        server_connection = f'DRIVER={{SQL Server}}; SERVER={getenv("SERVER")}; DATABASE={getenv("DATABASE")}; UID={getenv("USER")}; PWD={getenv("PASSWORD")}'
        try:
            _connection = connect(server_connection)
        except Error as e:
            logging.error(f"Erro ao conectar ao banco de dados: {e}")
            raise
    return _connection


def server_request(query: str, params=None) -> dict:
    """
    Executa uma query SQL com parâmetros para evitar SQL injection

    Args:
        query: Query SQL com placeholders para parâmetros (?)
        params: Tupla de parâmetros para substituir os placeholders

    Returns:
        dict: Dicionário com os resultados ou mensagem de erro
    """
    response = dict()

    try:
        connection = get_connection()
        with connection.cursor() as cursor:

            # Executa a query com parâmetros
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            # Para consultas do tipo SELECT
            if query.lower().strip().startswith('select'):
                columns = [column[0] for column in cursor.description]
                data = cursor.fetchall()

                # Converter para lista de dicionários para acesso mais claro
                result = []
                for row in data:
                    result.append(dict(zip(columns, row)))

                response['data'] = result
                response['message'] = 'Consulta executada com sucesso!'
            else:
                # Para INSERT, UPDATE, DELETE
                connection.commit()
                response['affected_rows'] = cursor.rowcount
                response['message'] = 'Script executado com sucesso!'

    except Error as e:
        logging.error(f"Erro de banco de dados: {e}")
        connection.rollback()  # Reverter alterações em caso de erro
        response['error'] = True
        response['message'] = 'Erro na conexão com o banco de dados'
    except Exception as e:
        logging.error(f"Erro inesperado: {e}")
        connection.rollback()  # Reverter alterações em caso de erro
        response['error'] = True
        response['message'] = 'Ocorreu um erro inesperado'

    return response


def close_connection():
    """Fecha a conexão com o banco de dados."""
    global _connection
    if _connection and not _connection.closed:
        _connection.close()
        _connection = None
