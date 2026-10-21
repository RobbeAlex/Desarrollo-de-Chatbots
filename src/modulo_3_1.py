from flask import Flask, request, jsonify 
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama # Cambia a langchain_openai si recargaste saldo
from langchain_core.output_parsers import StrOutputParser

app = Flask(__name__) 

# 1. Definición de reglas estáticas
RULES = {
    "calendario": "El calendario académico se encuentra publicado en el portal oficial.",
    "inscripcion": "El periodo de inscripción inicia la próxima semana."
}

# 2. Inicialización del modelo generativo (fuera de las funciones para mayor rendimiento)
prompt_template = ChatPromptTemplate.from_template(
    "Eres un asistente virtual útil. Responde de forma clara y concisa en español a la siguiente consulta: {pregunta}"
)
llm = ChatOllama(model="llama3.2", temperature=0.3) # Si usas OpenAI: ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
chain = prompt_template | llm | StrOutputParser()

def check_rules(text: str): 
    for k, v in RULES.items(): 
        if k in text.lower():
            return v 
    return None

def rag_fallback(text: str): 
    # 3. Integración real de LangChain para procesar la pregunta abierta
    try:
        respuesta_ia = chain.invoke({"pregunta": text})
        return respuesta_ia
    except Exception as e:
        return f"Ocurrió un error al procesar tu pregunta con la IA: {str(e)}"

@app.route("/", methods=["GET"])
def home():
    return "Servidor API funcionando correctamente."

@app.route("/api/chat", methods=["POST"]) 
def chat(): 
    data = request.json 
    msg = data.get("message", "")
    mode = data.get("mode", "hybrid") 

    # Modo rápido: Búsqueda por Reglas
    rule_ans = check_rules(msg)
    if rule_ans: 
        return jsonify({"answer": rule_ans, "mode_used": "rule_based", "latency": "0.025s"}) 

    # Fallback Híbrido: Generativo con LLM
    if mode == "hybrid": 
        ai_ans = rag_fallback(msg) 
        return jsonify({"answer": ai_ans, "mode_used": "llm_fallback", "latency": "Generativa"}) 

    return jsonify({"answer": "No reconozco el comando.", "mode_used": "default_fallback"}) 

if __name__ == "__main__": 
    app.run(port=5000)