import sqlite3
import pandas as pd;
def importar_csv_to_sqlitedb(conn, csv_path):
    """
        Toma un archivo csv y una conexion a la base de datos *ya creada con tablas que tienen nombres de columnas equivalentes a las columnas csv*. Luego llena todas las tablas con la data del csv.
    """
    

    #determinar tablas
    table_names = []
    for name in conn.execute("SELECT name FROM sqlite_master WHERE type='table';"):
        table_names.append(name[0])

    #popular data en cada tabla
    for table in table_names:

        conn.execute("DELETE FROM %s;"%(table))

        #gather columns names from table schema:
        columns = []
        for column in conn.execute("SELECT * FROM pragma_table_info(?);", (table,)):
            columns.append(column[1])

        #craft a sql statement for the table:

        csv_dataframe = pd.read_csv(csv_path) #this is the all the csv data, you can select specific columns like so: csv_dataframe[ ["ID", "edad", "ejemplo", "etc"] ]

        comma_sep_number_of_values = str.strip('?,'* len(columns),',')
        sql = f"INSERT INTO {table}({','.join(columns)}) VALUES ({comma_sep_number_of_values});"
        
        #execute that shit on all the data at once
        conn.executemany(sql,csv_dataframe[columns].values)
        #ok boom, now next table ->


        
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
def analizar_sentiment(texto):
    if not texto:
        return ""

    llm = Ollama(model="codegemma")
    prompt = ChatPromptTemplate.from_messages([
    ("system", """
        Analyze the sentiment of the input.
        Expected output schema: positive | negative
        Conform to the output schema.
        example: input = "Si", output = positive
    """),
    ("user", "{input}")
    ])
    chain = prompt | llm
    results = chain.invoke({"input":texto})    

    return results


import os
def normalizar(conn, csv_path, db_file):
    """
        only used once to import all data and correct encoding errors. 
    """
    importar_csv_to_sqlitedb(conn, csv_path)
    
    #drop me to a sqlite prompt to check changes:
    os.system("sqlite3 %s"%(db_file))
    if input("confirm changes? [y/n]: ") == "y":
        conn.commit()

def insert_sentiment(conn ,id, sentimiento):
    print(id, sentimiento)
    update_sql = "UPDATE Vehiculos_Electricos SET Sentimiento = :sentimiento WHERE ID_encuestado = :id;"
    params = {"sentimiento":sentimiento,"id":id}
    #check if column exists
    columns = [column[1] for column in conn.execute("SELECT * FROM pragma_table_info('Vehiculos_Electricos');")]

    if "Sentimiento" not in columns:
        conn.execute("ALTER TABLE Vehiculos_Electricos ADD COLUMN Sentimiento VARCHAR(10)")

    return conn.execute(update_sql, params).rowcount
    
    
    

def main():
    sqlite_file = "Encuesta_Grupo4.sql"
    conn = sqlite3.connect(sqlite_file)

    for resultado in conn.execute("SELECT ID_encuestado,Opinion_Vehiculo_Electrico from Vehiculos_Electricos;"):
        sentimiento = analizar_sentiment(resultado[1])
        
        while sentimiento not in ("positive","negative",""):
            print("retry on %s:'%s'"%(resultado[0],resultado[1]))
            sentimiento = analizar_sentiment(resultado[1])

        count = insert_sentiment(conn, resultado[0], sentimiento)

        if count:
            print("inserted %s:%s\n"%(resultado[0],sentimiento))
        else:
            print("did not insert.")

    if input("confirm changes? [y/n]: ") == "y":
        conn.commit()

    conn.close()




if __name__ == "__main__":
    main()