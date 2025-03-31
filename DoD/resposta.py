import operationsBD
import os
from dotenv import load_dotenv
load_dotenv()

from groq import Groq
client = Groq(api_key=os.getenv("GROQ_API_KEY"),)

contexto = "you are an AI assistant (the question and the answer will both be given in brazilian portuguese) for a person who takes care of an alzheimer's pacient and the caretaker asks you: "
modelo1 = "llama-3.3-70b-versatile"
modelo2 = "gemma2-9b-it"

def llmApi(p, m):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": contexto + p,
            }
        ],
        model=m,
    )
    resposta = chat_completion.choices[0].message.content
    return resposta

def responder(p):
    operationsBD.salvarPergunta(p)
    resposta1texto = llmApi( p, modelo1)
    resposta2texto = llmApi( p, modelo2)
    rag = False
    
    print("\n\n ########## RESPOSTA 1 ########## \n\n", resposta1texto , "\n\n ########## RESPOSTA 2 ########## \n\n",  resposta2texto)

    perguntaID = operationsBD.getPerguntaID(p)

    print("Agora avalie as respostas de acordo com os critérios solicitados")
    print("\nPrimeiro a RESPOSTA 1: ")
    relevancia1nota = input("Avalie de 1 a 5 a relevancia da resposta 1: \n")
    relevancia1texto = input("Justifique sua nota: \n")
    coerencia1nota = input("Avalie de 1 a 5 a coerência da resposta 1: \n")
    coerencia1texto = input("Justifique sua nota: \n")
    fluencia1nota = input("Avalie de 1 a 5 a fluência da resposta 1: \n")
    fluencia1texto = input("Justifique sua nota: \n")
    utilidade1nota = input("Avalie de 1 a 5 a utilidade da resposta 1: \n")
    utilidade1texto = input("Justifique sua nota: \n")
    etica1nota = input("Avalie de 1 a 5 a ética da resposta 1: \n")
    etica1texto = input("Justifique sua nota: \n")
    print("\nAGORA A RESPOSTA 2: ")
    relevancia2nota = input("Avalie de 1 a 5 a relevancia da resposta 2: \n")
    relevancia2texto = input("Justifique sua nota: \n")
    coerencia2nota = input("Avalie de 1 a 5 a coerência da resposta 2: \n")
    coerencia2texto = input("Justifique sua nota: \n")
    fluencia2nota = input("Avalie de 1 a 5 a fluência da resposta 2: \n")
    fluencia2texto = input("Justifique sua nota: \n")
    utilidade2nota = input("Avalie de 1 a 5 a utilidade da resposta 2: \n")
    utilidade2texto = input("Justifique sua nota: \n")
    etica2nota = input("Avalie de 1 a 5 a ética da resposta 2: \n")
    etica2texto = input("Justifique sua nota: \n")

    media1 = (int(relevancia1nota) + int(coerencia1nota) + int(fluencia1nota) + int(utilidade1nota) + int(etica1nota)) / 5
    media2 = (int(relevancia2nota) + int(coerencia2nota) + int(fluencia2nota) + int(utilidade2nota) + int(etica2nota)) / 5
    
    dataR1 = [
        media1,
        relevancia1nota,
        relevancia1texto,
        coerencia1nota,
        coerencia1texto,
        fluencia1nota,
        fluencia1texto,
        utilidade1nota,
        utilidade1texto,
        etica1nota,
        etica1texto,
        rag,
        resposta1texto,
        modelo1,
        perguntaID        
    ]
    
    dataR2 = [
        media2,
        relevancia2nota,
        relevancia2texto,
        coerencia2nota,
        coerencia2texto,
        fluencia2nota,
        fluencia2texto,
        utilidade2nota,
        utilidade2texto,
        etica2nota,
        etica2texto,
        rag,
        resposta2texto,
        modelo2,
        perguntaID    
    ]
    
    operationsBD.salvarResposta(dataR1, dataR2)