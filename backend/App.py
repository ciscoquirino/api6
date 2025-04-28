import resposta
import os
from dotenv import load_dotenv
load_dotenv()

from groq import Groq
client = Groq(api_key=os.getenv("GROQ_API_KEY"),)

pergunta = input("Digite sua pergunta: ")
resposta.responder(pergunta)




    
    

