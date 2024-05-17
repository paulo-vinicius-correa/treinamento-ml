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

with engine.connect() as conn:
    try:
        print("\n Tentando deletar...", end="")
        conn.execute(sqlalchemy.text( "delete from tb_book_sellers where dt_ref = '{date}'".format(date=date) ))
        print("ok.")
    except:
        print("Erro ao tentar deletar:")

    try:
        print("\n Tentando criar tabela...", end="")
        conn.execute(sqlalchemy.text('create table tb_book_sellers as\n {query}'.format(query=query)))
        conn.commit()
        print("ok.")

    except:
        print("Erro ao tentar criar tabela:")
        try:
            print("\n Tabela já existente, inserindo dados...", end="")
            conn.execute(sqlalchemy.text('insert into tb_book_sellers \n {query}'.format(query=query)))
            conn.commit()
            print("ok.\n")
        except:
            print("Erro ao inserir dados:")