import pandas as pd
import sqlalchemy 
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--date', '-d', help="Data para referencia de safra. Formato YYYY-MM-DD", default='2017-04-01')
args = parser.parse_args()
date = args.date

# Definindo os diretórios de trabalho
EP_DIR = os.path.dirname(os.path.abspath(__file__))  # Diretório do script atual
SRC_DIR = os.path.dirname(EP_DIR)  # Diretório pai do script
BASE_DIR = SRC_DIR  # O diretório base é o mesmo que o diretório pai
DATA_DIR = os.path.join(BASE_DIR, 'data')  # Diretório para armazenar dados
QUERY_DIR = os.path.join(BASE_DIR, 'sql')  # Diretório para armazenar consultas SQL

# importar consulta SQL de um arquivo
def import_query(path, **kwargs):
    with open(path, 'r', **kwargs) as file_open:
        result = file_open.read()
    return result

# conectar ao banco de dados SQLite
def connect_db():
    # Criando uma conexão com o banco de dados SQLite
    return sqlalchemy.create_engine("sqlite:///" + os.path.join(DATA_DIR, 'olist.db'))

# Importando a consulta safra.sql
query = import_query(os.path.join(QUERY_DIR, 'query1.sql'))
query = query.format(date=date)

# Estabelecendo uma conexão com o banco de dados
engine = connect_db()

try:
    with engine.connect() as conn:
        # Verificar se existem dados para a data especificada
        result = conn.execute(sqlalchemy.text("SELECT COUNT(*) FROM tb_book_sellers WHERE dt_ref = :date"), {'date': date}).fetchone()
        count = result[0]
        
        if count > 0:
            # Se existirem dados, exclua-os
            print("Tentando deletar registros existentes para a data especificada...", end="")
            conn.execute(sqlalchemy.text("DELETE FROM tb_book_sellers WHERE dt_ref = :date"), {'date': date})
            print("Registros deletados.")
        else:
            print("Nenhum registro encontrado para a data especificada.")

    # Inserir novos dados
    print("Inserindo novos dados...")
    pd.read_sql_query(query, engine).to_sql('tb_book_sellers', engine, if_exists='append', index=False)
    print("Novos dados inseridos com sucesso.")

except sqlalchemy.exc.SQLAlchemyError as e:
    print(f"Ocorreu um erro de SQLAlchemy: {str(e)}")
except Exception as e:
    print(f"Ocorreu um erro: {str(e)}")

conn.close()
