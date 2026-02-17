from flask import Flask
from urllib.parse import unquote_plus
app = Flask(__name__)
messages_db = ["Bienvenue !"]


def gen_html(messages):
    html_content = "<html><body><h1>Tchat minimaliste</h1><ul>"
    for msg in messages:
        html_content+="</ul></body></html>"
        return html_content

def add_message(messages, text):
    messages.append(text)

def remove_message(messages, index):
    messages.pop(index)

@app.route('/', methods=["GET"])
def index(): 
    return gen_html(messages_db)

@app.route('/<message>', methods=["POST"])
def post_msg(message):
    decoded_msg = unquote_plus(message)
    add_message(messages_db, decoded_msg)
    return f"Message '{decoded_msg}' ajouté.", 201

@app.route('/<int:indice>', methods=["DELETE"])
def delete_msg(indice):
    remove_message(messages_db, indice)
    return f"Message {indice} supprimé.", 200

if __name__ == '__main__':
    app.run(port=5000)