from flask import Flask, request
import wikipedia
import urllib.parse  # Importamos para decodificar la URL

app = Flask(__name__)
wikipedia.set_lang("es")

@app.route("/")
def respuesta():
    # Decodificamos el parámetro 'q' para manejar espacios y caracteres especiales
    q = urllib.parse.unquote(request.args.get("q", "")).strip()
    
    if not q:
        return "Por favor, escribe una búsqueda completa después del comando."
    
    try:
        # Buscamos sugerencias primero para manejar términos ambiguos
        sugerencias = wikipedia.search(q, results=3)
        if not sugerencias:
            return f"No encontré resultados para '{q}'."
        
        # Usamos el primer resultado de búsqueda
        resumen = wikipedia.summary(sugerencias[0], sentences=2)
        return resumen[:400]
        
    except wikipedia.exceptions.DisambiguationError as e:
        # Manejo de páginas de desambiguación
        opciones = e.options[:3]  # Mostramos solo 3 opciones
        return f"Hay varias opciones: {', '.join(opciones)}"
        
    except Exception as e:
        return f"No pude encontrar información sobre '{q}'. Error: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
