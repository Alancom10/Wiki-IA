from flask import Flask, request
import wikipedia
import urllib.parse

app = Flask(__name__)
wikipedia.set_lang("es")

@app.route("/search/<path:q>")  # ¡Asegúrate de incluir /search/!
def respuesta(q):
    q = urllib.parse.unquote(q).replace("+", " ").strip()  # Convierte "leon+s+kennedy" → "leon s kennedy"
    try:
        return wikipedia.summary(q, auto_suggest=False, sentences=2)[:400]
    except wikipedia.exceptions.PageError:
        return f"No encontré '{q}'. ¿Quisiste decir algo más?"
    except Exception as e:
        return "Error al buscar. Prueba más tarde."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
