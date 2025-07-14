from flask import Flask, request
import wikipedia
import urllib.parse

app = Flask(__name__)
wikipedia.set_lang("es")

@app.route("/<path:busqueda>")  # Captura TODO después de la barra (/)
def respuesta(busqueda):
    q = urllib.parse.unquote(busqueda).strip()  # Decodifica "Leon%20S.%20Kennedy" → "Leon S. Kennedy"
    try:
        return wikipedia.summary(q, auto_suggest=False, sentences=2)[:400]
    except:
        return f"No encontré '{q}'. Prueba con comillas: !p \"{q}\""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
