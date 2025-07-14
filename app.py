from flask import Flask, request
import wikipedia
import urllib.parse

app = Flask(__name__)
wikipedia.set_lang("es")

@app.route("/search/<path:q>")
def respuesta(q):
    try:
        q = urllib.parse.unquote(q).replace("+", " ").strip().lower()
        
        # Paso 1: Búsqueda con sugerencias (para términos ambiguos)
        sugerencias = wikipedia.search(q, results=3)
        if not sugerencias:
            return f"🔍 No encontré '{q}'. Prueba con: !p \"Término exacto\""
        
        # Paso 2: Usar el primer resultado relevante
        pagina = wikipedia.page(sugerencias[0], auto_suggest=False)
        return f"📚 {pagina.title}: {pagina.summary[:350]}..."  # Límite de caracteres
        
    except wikipedia.exceptions.DisambiguationError:
        return f"⚠️ Hay múltiples opciones para '{q}'. Sé más específico."
    except Exception as e:
        return f"❌ Error: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
