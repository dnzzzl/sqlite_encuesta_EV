# sqlite_encuesta_EV
SQLite database para la data recolectada en la encuesta de Vehiculos Electricos. Actividad realizada para el curso Big Data Analytics.

---

# Tarea Realizada: Analisis de sentimiento con Open Source AI:
   - Ciertos caracteres con tilde española están mal formados dentro de la base de datos sqlite.

### Tareas:
   - Limpiar datos mal formados: reescribir palabras para que no tengan tilde.
   - Agregar columna dentro de la tabla Vehiculos_Electricos llamada "Sentimiento" para almacenar análisis de sentimiento
   - Realizar análisis de sentimiento con IA y almacenar los resultados de cada entrada

---

### Task One: Clean malformed data:
 ## goals:
    - reescribir el las entradas de la base de datos desde los datos originales para corregir errores de encodificacion
    
### Task Two: Sentiment analysis:
 **goals**:
 
     - create a column for sentiment analysis, perform analysis and store the results.

  **steps**:
    
     1. load langchain library and setup connection to local LLM
     2. setup prompt for input of each entry to the LLM
     3. using sqlite api run through each entry and insert result in the specified column.
     4. profit.
