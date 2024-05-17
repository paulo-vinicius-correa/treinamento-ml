import pandas as pd
import sqlalchemy 
import os
from sklearn import metrics
from sklearn import tree

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
query = import_query(os.path.join(QUERY_DIR, 'safra.sql'))

# Estabelecendo uma conexão com o banco de dados
con = connect_db()

# Executando a consulta SQL e carregando os resultados em um DataFrame
df = pd.read_sql(query, con)
columns = df.columns.tolist()

# seta as variaveis que devem ser removidas
to_remove = ['seller_id','seller_city']

#variavel alvo
target = 'flag_model'

# remove de fato as variáveis se elas estiverem na lista de colunas
columns = [col for col in columns if col not in to_remove + [target]]

#define os tipos de variaveis
cat_features = df[columns].dtypes[df[columns].dtypes == 'object'].index.tolist()
num_features = list(set(columns) - set(cat_features))

clf = tree.DecisionTreeClassifier(max_depth=10)
clf.fit(df[num_features], df[target])

y_pred = clf.predict(df[num_features])
y_prod = clf.predict_proba(df[num_features])

metrics.confusion_matrix ( df[target], y_pred )
print(metrics.confusion_matrix ( df[target], y_pred ))