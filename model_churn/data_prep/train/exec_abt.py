import os
import sqlalchemy

# Obter o diretório do script atual
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PREP_DIR = os.path.dirname(SCRIPT_DIR)
MODEL_CHURN_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))
DATA_DIR = os.path.dirname(os.path.dirname(os.path.dirname(SCRIPT_DIR)))

# conectar ao banco de dados SQLite
def connect_db():
    # Criando uma conexão com o banco de dados SQLite
    return sqlalchemy.create_engine("sqlite:///" + os.path.join(DATA_DIR, 'olist.db'))

# Estabelecendo uma conexão com o banco de dados
engine = connect_db()

with engine.connect() as conn:
    with open(os.path.join(SCRIPT_DIR, 'var_resposta.sql'),'r') as open_file:
        query = open_file.read()

    for i in query.split(";")[:-1]:
        conn.execute( i )
