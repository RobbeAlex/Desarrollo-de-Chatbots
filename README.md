# 💬 Desarrollo de Chatbots: De Motores de Reglas a RAG y Grafos de Estado (LangGraph)

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-LCEL-1C3C3C?style=flat)](https://www.langchain.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-StateGraph-FF6F00?style=flat)](https://langchain-ai.github.io/langgraph/)
[![Qdrant](https://img.shields.io/badge/Qdrant-Vector%20DB-DC244C?style=flat)](https://qdrant.tech/)
[![Flask](https://img.shields.io/badge/Flask-REST%20API-000000?style=flat&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Repositorio práctico y progresivo sobre el diseño e implementación de **sistemas conversacionales inteligentes**. Abarca la evolución arquitectónica completa: desde motores deterministas tolerantes a errores tipográficos y flujos transaccionales basados en *slots*, hasta pipelines de **Generación Aumentada por Recuperación (RAG)** con bases vectoriales (**Qdrant**), cadenas declarativas con **LangChain + Ollama**, máquinas de estado con **LangGraph** y un **Gateway Híbrido en Flask**.

> 📘 **¿Buscas el detalle arquitectónico de cada componente?** Consulta la [Documentación Técnica (`DOCUMENTACION_TECNICA.md`)](DOCUMENTACION_TECNICA.md).

---

## 🧭 Evolución de los Módulos del Proyecto

| Módulo | Archivo | Paradigma / Tecnología | Descripción Funcional |
| :---: | :--- | :--- | :--- |
| **1.1** | [`modulo_1_1.py`](modulo_1_1.py) | **Motor de Reglas Difuso (`difflib`)** | Implementa la clase `RuleEngine` que compara tokens del usuario contra una base de conocimiento usando similitud de cadenas (`cutoff=0.6`), tolerando faltas de ortografía (ej. *"orario"* $\rightarrow$ *"horario"*). |
| **1.2** | [`config/modulo_1_2.yml`](config/modulo_1_2.yml) | **Flujos Conversacionales Declarativos (YAML)** | Define el flujo transaccional `transferir_monto` con recolección secuencial de *slots* (`destinatario`, `monto`), verificación de fondos (`action_check_sufficient_funds`) y confirmación explícita. |
| **2.1** | [`modulo_2_1.py`](modulo_2_1.py) | **Pipeline RAG con Qdrant + OpenAI** | Crea la colección vectorial `documentos_empresa` (`1536` dims, distancia Coseno), fragmenta documentos (`chunk_size=512`, `overlap=50`), indexa embeddings (`text-embedding-3-small`) y responde con `gpt-4o-mini`. |
| **2.2** | [`modulo_2_2.py`](modulo_2_2.py) | **LangChain LCEL + LLM Local (Ollama)** | Construye una cadena declarativa (`ChatPromptTemplate \| ChatOllama \| StrOutputParser`) ejecutando inferencia local privada con `llama3.2`. |
| **2.3** | [`modulo_2_3.py`](modulo_2_3.py) | **Agentes Basados en Grafos (`LangGraph`)** | Implementa un `StateGraph` sobre `AgentState` (`history`, `sentiment`) con ruteo condicional automático hacia soporte técnico humano cuando detecta sentimiento negativo o errores. |
| **3.1** | [`modulo_3_1.py`](modulo_3_1.py) | **Gateway API Híbrido (`Flask` + `LangChain`)** | Expone el endpoint `POST /api/chat` que combina la velocidad de reglas estáticas (`~0.025s`) con un *fallback* generativo en LangChain/Ollama para preguntas abiertas. |

---

## 🛠️ Requisitos Previos

1. **Python 3.10+**
2. **Ollama** (para los módulos `2.2` y `3.1`):
   ```bash
   ollama run llama3.2
   ```
3. **Qdrant Vector Database** (para el módulo `2.1`):
   ```bash
   docker run -d -p 6333:6333 -v ./database/qdrant_storage:/qdrant/storage qdrant/qdrant
   ```
4. **API Key de OpenAI** (para el módulo `2.1`):
   Configura la variable de entorno `OPENAI_API_KEY` en tu sistema o en un archivo `.env`.

---

## ⚙️ Instalación

1. **Crear y activar un entorno virtual**:
   ```bash
   python -m venv venv
   # En Windows:
   venv\Scripts\activate
   # En Linux/macOS:
   source venv/bin/activate
   ```

2. **Instalar las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ Guía de Ejecución por Módulo

```bash
# Módulo 1.1: Prueba de concordancia difusa basada en reglas
python src/modulo_1_1.py

# Módulo 2.1: Pipeline RAG con Qdrant y OpenAI (requiere Qdrant en :6333 y OPENAI_API_KEY)
python src/modulo_2_1.py

# Módulo 2.2: Inferencia declarativa con LangChain y Ollama (llama3.2)
python src/modulo_2_2.py

# Módulo 2.3: Compilación del grafo de estados condicional con LangGraph
python src/modulo_2_3.py

# Módulo 3.1: Servidor API Híbrido en Flask (http://localhost:5000)
python src/modulo_3_1.py
```

### Ejemplo de Petición al Gateway Híbrido (`modulo_3_1.py`)

```bash
# 1. Consulta resuelta por regla estática (baja latencia)
curl -X POST http://localhost:5000/api/chat \
     -H "Content-Type: application/json" \
     -d "{\"message\": \"¿Dónde veo el calendario académico?\", \"mode\": \"hybrid\"}"

# 2. Consulta abierta derivada automáticamente al LLM (fallback generativo)
curl -X POST http://localhost:5000/api/chat \
     -H "Content-Type: application/json" \
     -d "{\"message\": \"Explícame cómo funciona una base de datos vectorial\", \"mode\": \"hybrid\"}"
```

---

## 📄 Licencia y Autor

Distribuido bajo la **Licencia MIT**. Consulta el archivo [LICENSE](LICENSE) para más información.

**Autor:** Roberto Alejandro Chagra Martínez — *Universidad de Guadalajara (UdeG)*
