import os
from dotenv import load_dotenv
load_dotenv()

import psycopg2

conexao = psycopg2.connect(os.getenv("DB_URI"))

def salvarPergunta(x):
    try:
        cursor = conexao.cursor()
        cursor.execute(f"INSERT INTO pergunta (texto) VALUES ('{x}');")

        conexao.commit()
        
        cursor.close()
    except psycopg2.Error as erro:
        print("Erro ao conectar ao PostgreSQL:", erro)
        
def getPerguntaID(x):
    try:
        cursor = conexao.cursor()
        cursor.execute(f"SELECT MAX(id) FROM pergunta WHERE texto = '{x}';")
        result = cursor.fetchone()
        id = result[0]
        cursor.close()

        return id
    except psycopg2.Error as erro:
        print("Erro ao conectar ao PostgreSQL:", erro)    
        
def salvarResposta(r1, r2):
    try:
        cursor = conexao.cursor()
        cursor.execute('''INSERT INTO resposta 
                       (media, 
                        relevancia_nota, 
                        relevancia_texto, 
                        coerencia_nota, 
                        coerencia_texto, 
                        fluencia_nota, 
                        fluencia_texto, 
                        utilidade_nota, 
                        utilidade_texto,
                        etica_nota,
                        etica_texto,
                        rag,
                        texto,
                        modelo,
                        fk_pergunta_id) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);''', r1)

        cursor.execute('''INSERT INTO resposta 
                       (media, 
                        relevancia_nota, 
                        relevancia_texto, 
                        coerencia_nota, 
                        coerencia_texto, 
                        fluencia_nota, 
                        fluencia_texto, 
                        utilidade_nota, 
                        utilidade_texto,
                        etica_nota,
                        etica_texto,
                        rag,
                        texto,
                        modelo,
                        fk_pergunta_id) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);''', r2)
        conexao.commit()
        
        cursor.close()
    except psycopg2.Error as erro:
        print("Erro ao conectar ao PostgreSQL:", erro)