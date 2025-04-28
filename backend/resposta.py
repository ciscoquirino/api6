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

def previsaoLikert(m):
    return round(3 + 2 * ( m ))

def chat1(p, r1, r2):
    perguntaID = operationsBD.getPerguntaID(p)
    rag = False

    print("\n\n ########## RESPOSTA A ########## \n\n", r1 , "\n\n ########## RESPOSTA B ########## \n\n",  r2 , "----------------------------------------------")

    print("Agora avalie as respostas de acordo com os critérios solicitados")
    print("\nPrimeiro a RESPOSTA A: ")
    relevancia1nota = input("Avalie de 1 a 5 a instrução da resposta A, sendo *1 = não atende à sua questão* e *5 = atende completamente*: \n")
    relevancia1texto = input("Justifique sua nota: \n")
    linguagem1nota = input("Avalie de 1 a 5 a linguagem da resposta A, sendo *1 = linguagem não natural / idioma incorreto* e *5 = linguagem natural / idioma correto* : \n")
    linguagem1texto = input("Justifique sua nota: \n")
    veracidade1nota = input("Avalie de 1 a 5 a veracidade da resposta A, sendo *1 = não verdadeiro* e *5 = completamente verdadeiro*: \n")
    veracidade1texto = input("Justifique sua nota: \n")
    etica1nota = input("Avalie de 1 a 5 a ética da resposta A, sendo *1 = nociva / inadequada* e *5 = sem nocividade, cordial e adequada* \n")
    etica1texto = input("Justifique sua nota: \n")
    print("\nAGORA A RESPOSTA B: ")
    relevancia2nota = input("Avalie de 1 a 5 a instrução da resposta B, sendo *1 = não atende à sua questão* e *5 = atende completamente*: \n")
    relevancia2texto = input("Justifique sua nota: \n")
    linguagem2nota = input("Avalie de 1 a 5 a linguagem da resposta B, sendo *1 = linguagem não natural / idioma incorreto* e *5 = linguagem natural / idioma correto* : \n")
    linguagem2texto = input("Justifique sua nota: \n")
    veracidade2nota = input("Avalie de 1 a 5 a veracidade da resposta B, sendo *1 = não verdadeiro* e *5 = completamente verdadeiro*: \n")
    veracidade2texto = input("Justifique sua nota: \n")
    etica2nota = input("Avalie de 1 a 5 a ética da resposta B, sendo *1 = nociva / inadequada* e *5 = sem nocividade, cordial e adequada* \n")
    etica2texto = input("Justifique sua nota: \n")

    m1 = (int(relevancia1nota) + int(linguagem1nota) + int(veracidade1nota) + int(etica1nota)) / 4
    m2 = (int(relevancia2nota) + int(linguagem2nota) + int(veracidade2nota) + int(etica2nota)) / 4
    #normalização das médias de cada resposta
    media1 = (m1 - 1) / 4
    media2 = (m2 - 1) / 4

    dataR1 = [
        media1,
        relevancia1nota,
        relevancia1texto,
        linguagem1nota,
        linguagem1texto,
        veracidade1nota,
        veracidade1texto,
        etica1nota,
        etica1texto,
        rag,
        r1,
        modelo1,
        perguntaID        
    ]
    
    dataR2 = [
        media2,
        relevancia2nota,
        relevancia2texto,
        linguagem2nota,
        linguagem2texto,
        veracidade2nota,
        veracidade2texto,
        etica2nota,
        etica2texto,
        rag,
        r2,
        modelo2,
        perguntaID    
    ]

    return dataR1, dataR2

def chat2():
    print("\n\n AGORA SELECIONE A MELHOR RESPOSTA DE FORMA GERAL: \n\n")
    print()
    rlikert = input('''Digite um número de 1 a 5, sendo:
        1 = Resposta A é muito melhor
        2 = Resposta A é melhor
        3 = Indiferente, ambas respostas tem a mesma qualidade
        4 = Resposta B é melhor
        5 = Resposta B é muito melhor
    \n''')
    
    rTexto = input("\nJustifique sua resposta: \n")
    return rlikert, rTexto

def checarCoerencia(rc, dr1, dr2):
    
    pontuacao_relativa = dr2[0] - dr1[0]
    pLikert = previsaoLikert(pontuacao_relativa)

    if int(rc) != int(pLikert):
        print("\n\nParece que sua escolha final foi incoerente com as avaliações que você deu para as respostas.")
        print(f"Você indicou: {rc} na pergunta final.")
        print(f"Pela sua avaliação, o esperado seria: {pLikert}.")
        
        opcao = input("\nDeseja:\n1 - Corrigir apenas nota final\n2 - Reavaliar as respostas\nDigite 1 ou 2: ")
        
        while opcao not in ["1", "2"]:
            opcao = input("Opção inválida. Digite 1 para corrigir a nota final ou 2 para reavaliar: ")

        if opcao == "1":
            novo_rc, novo_tc = chat2()
            return int(novo_rc), novo_tc, dr1, dr2
        else:
            # Reavaliar tudo novamente
            dr1, dr2 = chat1("", dr1[10], dr2[10]) 
            novo_rc, novo_tc = chat2()
            return int(novo_rc), novo_tc, dr1, dr2

    # Se for coerente, apenas continua
    return int(rc), None, dr1, dr2



def responder(p):
    operationsBD.salvarPergunta(p)
    resposta1texto = llmApi(p, modelo1)
    resposta2texto = llmApi(p, modelo2)
    
    dr1 , dr2 = chat1(p, resposta1texto, resposta2texto)
    
    rc, tc= chat2()

    rc, tc_corrigido, dr1, dr2 = checarCoerencia(rc, dr1, dr2)

    
    if tc_corrigido is not None:
        tc = tc_corrigido
    
    operationsBD.salvarResposta(dr1, dr2)

    idr1 = operationsBD.getRespostaID(dr1[10])
    idr2 = operationsBD.getRespostaID(dr2[10])
    
    dataComp = [idr1, idr2, rc, tc]

    operationsBD.salvarComparacao(dataComp)

    print("\n\nOk! Obrigado pela sua avaliação!")
    
