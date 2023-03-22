from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from bd import contatos

import secrets as sct

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})

def create_token():
    return (sct.token_hex())

@app.route('/contatos', methods=["GET"])
def get_contatos():
    response = jsonify(contatos)
    response.headers['token'] = str(create_token())
    return response, 200

@app.route('/contatos/<int:id>', methods=["GET"])
def get_contato_by_id(id):
    contato = None
    for ct in contatos:
        if ct["id"] == id:
            contato = ct
    if contato != None:
        response = jsonify(contato)
        response.headers['token'] = str(create_token())
        return response, 200
    else:
        return 'Contato não encontrado'

@app.route('/contatos', methods=["POST"])
def create_contato():
    contato = request.get_json(force=True)
    contatos.append(contato)
    response = jsonify(
        msg = 'Contato cadastrado com sucesso',
        contato=contato
        )
    response.headers['token'] = str(create_token())
    return response, 201
    

@app.route('/deletar/<int:id>', methods=["DELETE"])
def deletar_contato(id):
    response = Response()
    response.headers['token'] = str(create_token)
    for ct in contatos:
        if ct['id'] == id:
            index = contatos.index(ct)
            contatos.pop(index)
            response = jsonify(
                msg = f"Contato de ID {id} excluido com sucesso"
            )
            response.headers['token'] = str(create_token())
            return response
    
    return jsonify({"Erro: contato não encontrado"})

@app.route('/contatos/<int:id>', methods=["PUT"])
def update_contato_by_id(id):
    response = Response()
    response.headers['token'] = str(create_token)
    index = id
    deletar_contato(id)
    contato = request.get_json(force=True)
    contato['id'] = index
    contatos.append(contato)
    response = jsonify(
        msg = f"Contato de ID {index} atualizado com sucesso",
        contato=contato
    )
    response.headers['token'] = str(create_token())
    return response

@app.route("/contatos/<int:id>", methods=["PATCH"])
def update_numero_by_id(id):
    res = Response()
    res.headers['token'] = str(create_token())

    contato = None
    for ct in contatos:
        if ct['id'] == id:
            index = contatos.index(ct)
            contato = ct
            contatos.pop(index)

    novo_numero = request.get_json(force=True)
    contato['numero'] = novo_numero['numero']
    contato['id'] = index

    contatos.append(contato)
    return res

@app.route('/head', methods=["HEAD"])
def get_head():
    res = Response()
    res = jsonify(
        dict(res.headers)
    )
    res.headers['token'] = str(create_token())
    print(dict(res.headers))
    return res

@app.route('/options', methods=["OPTIONS"])
def get_options():
    response = Response()
    acao = str(response.headers.get("Access-Control-Allow-Origin"))
    response.headers["X-Content-Type-Options"] = "*"
    response.headers['token'] = str(create_token())
    print(dict(response.headers))
    return response

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")