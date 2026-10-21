import difflib

class RuleEngine:
    def __init__(self, knowledge_base: dict):
        self.kb = knowledge_base

    def get_response(self, user_input: str, cutoff: float = 0.6) -> str:
        words = user_input.lower().split()
        for word in words:
            matches = difflib.get_close_matches(word, self.kb.keys(), n=1, cutoff=cutoff)
            if matches:
                return self.kb[matches[0]]
        return "Disculpe, no tengo información para esa consulta."

kb = {
    "horario": "El horario de atención es de lunes a viernes de 08:00 a 17:00.",
    "requisitos": "Los requisitos de inscripción son identificación oficial y comprobante."
}

bot = RuleEngine(kb)
print(bot.get_response("¿cuál es el orario de atención?"))