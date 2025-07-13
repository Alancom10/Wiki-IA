from flask import Flask, request
import wikipedia  # ✅ Importamos Wikipedia

app = Flask(__name__)
wikipedia.set_lang("es")  # ✅ Indicamos que las respuestas sean en español


@app.route("/")
def respuesta():
    q = request.args.get("q", "")
    if not q:
        return "Tenés que escribir una pregunta."
    try:
        resumen = wikipedia.summary(q, sentences=2)
        return resumen[:
                       400]  # ✅ Recortamos para que no supere los límites del chat de Twitch
    except:
        return "No encontré información sobre eso."


import os

print("Nombre del Repl:", os.environ.get('REPL_SLUG'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
