import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()
DB_URI = os.getenv("DB_URI")

def salvarPergunta(x):
    try:
        with psycopg2.connect(DB_URI) as conn:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO pergunta (texto) VALUES (%s);", (x,))
    except psycopg2.Error as erro:
        print("Erro ao conectar ao PostgreSQL:", erro)

def getPerguntaID(x):
    try:
        with psycopg2.connect(DB_URI) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT MAX(id) FROM pergunta WHERE texto = %s;", (x,))
                result = cursor.fetchone()
                return result[0]
    except psycopg2.Error as erro:
        print("Erro ao conectar ao PostgreSQL:", erro)
        return None

def salvarResposta(r1, r2):
    try:
        with psycopg2.connect(DB_URI) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""INSERT INTO resposta 
                    (media, relevancia_nota, relevancia_texto, linguagem_nota, linguagem_texto, 
                     veracidade_nota, veracidade_texto, etica_nota, etica_texto, rag, texto, modelo, fk_pergunta_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""", r1)

                cursor.execute("""INSERT INTO resposta 
                    (media, relevancia_nota, relevancia_texto, linguagem_nota, linguagem_texto, 
                     veracidade_nota, veracidade_texto, etica_nota, etica_texto, rag, texto, modelo, fk_pergunta_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""", r2)
    except psycopg2.Error as erro:
        print("Erro ao conectar ao PostgreSQL:", erro)

def getRespostaID(x):
    try:
        with psycopg2.connect(DB_URI) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT MAX(id) FROM resposta WHERE texto = %s;", (x,))
                result = cursor.fetchone()
                return result[0]
    except psycopg2.Error as erro:
        print("Erro ao conectar ao PostgreSQL:", erro)
        return None

def salvarComparacao(d):
    try:
        with psycopg2.connect(DB_URI) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""INSERT INTO comparacao 
                    (fk_resposta1_id, fk_resposta2_id, pontuacao1, texto) 
                    VALUES (%s, %s, %s, %s);""", d)
    except psycopg2.Error as erro:
        print("Erro ao conectar ao PostgreSQL:", erro)
