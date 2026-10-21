from typing import TypedDict, List
from langgraph.graph import StateGraph, END

class AgentState(TypedDict): 
    history: List[str] 
    sentiment: str 
    
def sentiment_node(state: AgentState): 
    last_msg = state["history"][-1] if state["history"] else ""
    sentiment = "negative" if "error" in last_msg.lower() else "positive"
    return {"sentiment": sentiment} 

def route_sentiment(state: AgentState): 
    if state["sentiment"] == "negative":
        return "soporte"
    return "finalizar"

def soporte_node(state: AgentState):
    return {"history": state["history"] + ["Bot: Transferido con el equipo de soporte técnico."]}

def finalizar_node(state: AgentState):
    return {"history": state["history"] + ["Bot: ¡Gracias por tu consulta!"]} 

workflow = StateGraph(AgentState)
workflow.add_node("analizar", sentiment_node)
workflow.add_node("soporte", soporte_node) 
workflow.add_node("finalizar", finalizar_node)

workflow.set_entry_point("analizar")
workflow.add_conditional_edges("analizar", route_sentiment)
workflow.add_edge("soporte", END) 
workflow.add_edge("finalizar", END) 

app = workflow.compile()