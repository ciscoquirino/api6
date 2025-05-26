import resposta2
import operationsBD
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"]) 

@app.route("/api/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "")
    resposta = resposta2.responder(question)
    
    response_a = resposta[0]
    response_b = resposta[1]
    


    return jsonify({
        "responses": [response_a, response_b]
    })


@app.route("/api/evaluate", methods=["POST"])
def evaluate():
    data = request.get_json()

    pergunta = data['question']
    relevancia1nota = data['evaluations'][0]['Instrução']['score']
    relevancia1texto = data['evaluations'][0]['Instrução']['comment']
    linguagem1nota = data['evaluations'][0]['Linguagem']['score']
    linguagem1texto = data['evaluations'][0]['Linguagem']['comment']
    veracidade1nota = data['evaluations'][0]['Veracidade']['score']
    veracidade1texto = data['evaluations'][0]['Veracidade']['comment']
    etica1nota = data['evaluations'][0]['Ética']['score']
    etica1texto = data['evaluations'][0]['Ética']['comment']
    rag1 = data['responses'][0]['rag']
    texto1 = data['responses'][0]['resposta']
    modelo1 = data['responses'][0]['modelo']
    relevancia2nota = data['evaluations'][1]['Instrução']['score']
    relevancia2texto = data['evaluations'][1]['Instrução']['comment']
    linguagem2nota = data['evaluations'][1]['Linguagem']['score']
    linguagem2texto = data['evaluations'][1]['Linguagem']['comment']
    veracidade2nota = data['evaluations'][1]['Veracidade']['score']
    veracidade2texto = data['evaluations'][1]['Veracidade']['comment']
    etica2nota = data['evaluations'][1]['Ética']['score']
    etica2texto = data['evaluations'][1]['Ética']['comment']
    rag2 = data['responses'][1]['rag']
    texto2 = data['responses'][1]['resposta']
    modelo2 = data['responses'][1]['modelo']

    m1 = (int(relevancia1nota) + int(linguagem1nota) + int(veracidade1nota) + int(etica1nota)) / 4
    m2 = (int(relevancia2nota) + int(linguagem2nota) + int(veracidade2nota) + int(etica2nota)) / 4

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
        rag1,
        texto1,
        modelo1
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
        rag2,
        texto2,
        modelo2
    ]
    
    resposta2.salvarAvaliacao(pergunta, dataR1, dataR2)

    return jsonify({"message": "Avaliações recebidas com sucesso!"})

@app.route("/api/compare", methods=["POST"])
def compare():
    data = request.get_json()

    texto1 = data.get("resposta1", "")
    texto2 = data.get("resposta2", "")
    score = int(data.get("score", 3))
    comment = data.get("comment", "")

    id1 = operationsBD.getRespostaID(texto1)
    id2 = operationsBD.getRespostaID(texto2)

    operationsBD.salvarComparacao([id1, id2, score, comment])

    return jsonify({"message": "Comparação registrada com sucesso!"})



if __name__ == "__main__":
    app.run(debug=True)





    
    

