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
                        linguagem_nota, 
                        linguagem_texto, 
                        veracidade_nota, 
                        veracidade_texto, 
                        etica_nota,
                        etica_texto,
                        rag,
                        texto,
                        modelo,
                        fk_pergunta_id) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);''', r1)

        cursor.execute('''INSERT INTO resposta 
                       (media, 
                        relevancia_nota, 
                        relevancia_texto, 
                        linguagem_nota, 
                        linguagem_texto, 
                        veracidade_nota, 
                        veracidade_texto,
                        etica_nota,
                        etica_texto,
                        rag,
                        texto,
                        modelo,
                        fk_pergunta_id) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);''', r2)
        conexao.commit()
        
        cursor.close()
    except psycopg2.Error as erro:
        print("Erro ao conectar ao PostgreSQL:", erro)

def getRespostaID(x):
    try:
        cursor = conexao.cursor()
        cursor.execute(f"SELECT MAX(id) FROM resposta WHERE texto = '{x}';")
        result = cursor.fetchone()
        id = result[0]
        cursor.close()

        return id
    except psycopg2.Error as erro:
        print("Erro ao conectar ao PostgreSQL:", erro)  



def salvarComparacao(d):
    dados = d

    try:
        cursor = conexao.cursor()
        cursor.execute('''INSERT INTO comparacao 
                        (fk_resposta1_id, 
                        fk_resposta2_id, 
                        pontuacao1, 
                        texto) 
                        VALUES (%s, %s, %s, %s);''', dados)
        conexao.commit()
            
        cursor.close()
    except psycopg2.Error as erro:
        print("Erro ao conectar ao PostgreSQL:", erro)