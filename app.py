from flask import Flask, request
import wikipedia
import urllib.parse
from urllib.parse import unquote

app = Flask(__name__)
wikipedia.set_lang("es")
wikipedia.set_rate_limiting(True)  # Evita bloqueos por exceso de solicitudes

@app.route("/search/<path:query>")
def search(query):
    try:
        # Decodifica la consulta y maneja caracteres especiales
        search_term = unquote(query).replace("+", " ").strip()
        
        # Primero busca sugerencias para manejar términos ambiguos
        suggestions = wikipedia.search(search_term, results=1)
        if not suggestions:
            return f"No encontré resultados para '{search_term}'"
            
        # Obtiene el resumen de la primera sugerencia
        page = wikipedia.page(suggestions[0], auto_suggest=False)
        summary = wikipedia.summary(page.title, sentences=2)
        
        return f"{page.title}: {summary[:300]}..."  # Limita a 300 caracteres
        
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Hay múltiples opciones para '{search_term}': {', '.join(e.options[:3])}"
    except wikipedia.exceptions.PageError:
        return f"No encontré información sobre '{search_term}'"
    except Exception as e:
        print(f"Error interno: {str(e)}")  # Log para diagnóstico
        return "Error temporal. Por favor, intenta nuevamente."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
