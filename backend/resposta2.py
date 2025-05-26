import operationsBD
import random
import chromadb
import os
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
load_dotenv()


#RAG
client = chromadb.PersistentClient(path="client")
collection = client.get_collection(name='new_collection')
model = SentenceTransformer('all-MiniLM-L6-v2')


from groq import Groq
clientgroq = Groq(api_key=os.getenv("GROQ_API_KEY"),)

modelo1 = "llama-3.3-70b-versatile"
modelo2 = "gemma2-9b-it"

def rag(p, m):
    r = True
    query_embedding = model.encode([p])
    results = collection.query(query_embeddings=query_embedding, n_results=10)
    ragcontext = results['documents']
    contexto1 = "you are an AI assistant (the question and the answer will both be given in brazilian portuguese) for a person who takes care of an alzheimer's pacient and the caretaker asks you:  "
    contexto2 = ". Try to use the following texts to improve your answer: "
    chat_completion = clientgroq.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": contexto1 + p + contexto2 + str(ragcontext),
            }
        ],
        model=m,
    )
    texto = chat_completion.choices[0].message.content
    return {'resposta': texto, 'modelo': m, 'rag': r}

def llmApi(p, m):
    r = False
    contexto = "you are an AI assistant (the question and the answer will both be given in brazilian portuguese) for a person who takes care of an alzheimer's pacient and the caretaker asks you: "
    chat_completion = clientgroq.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": contexto + p,
            }
        ],
        model=m,
    )
    texto = chat_completion.choices[0].message.content
    return {'resposta': texto, 'modelo': m, 'rag': r}

def responder(p):
    operationsBD.salvarPergunta(p)
    r1 = llmApi(p, modelo1)
    r2 = llmApi(p, modelo2)
    r3 = rag(p, modelo1)
    r4 = rag(p, modelo2)
    i = random.randint(0, 5)

    match i:
        case 0:
            return r1, r2
        case 1:
            return r1, r3
        case 2:
            return r1, r4
        case 3:
            return r2, r3
        case 4:
            return r2, r4
        case 5:
            return r3, r4


def salvarAvaliacao(p, d1, d2):
    perguntaID = operationsBD.getPerguntaID(p)
    dados1 = d1 + [perguntaID]
    dados2 = d2 + [perguntaID]
    operationsBD.salvarResposta(dados1, dados2)