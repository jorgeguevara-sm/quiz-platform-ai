"""
Templates predefinidos por industria.
Formato identico al GeneratedTestSchema para reutilizar el mismo pipeline de persistencia.
"""

TEMPLATES = {
    "abogado_insolvencia": {
        "title": "Diagnostico: Ley de Insolvencia en Colombia",
        "industry": "legal",
        "language": "es",
        "questions": [
            {"type": "yes_no", "text": "Estas actualmente en Colombia como residente fiscal?",
             "options": [{"label": "Si", "value": "yes", "score": 2}, {"label": "No", "value": "no", "score": 0}], "weight": 1.0},
            {"type": "multiple_choice", "text": "Cual es tu nivel de endeudamiento actual?",
             "options": [
                 {"label": "Menos de 10 millones", "value": "low", "score": 1},
                 {"label": "Entre 10 y 50 millones", "value": "mid", "score": 3},
                 {"label": "Mas de 50 millones", "value": "high", "score": 5},
             ], "weight": 1.0},
            {"type": "yes_no", "text": "Tienes ingresos fijos comprobables?",
             "options": [{"label": "Si", "value": "yes", "score": 2}, {"label": "No", "value": "no", "score": 0}], "weight": 1.0},
            {"type": "yes_no", "text": "Has intentado negociar directamente con tus acreedores?",
             "options": [{"label": "Si", "value": "yes", "score": 1}, {"label": "No", "value": "no", "score": 2}], "weight": 1.0},
            {"type": "scale", "text": "Que tan urgente consideras tu situacion financiera (1-5)?",
             "options": [], "weight": 1.5},
            {"type": "multiple_choice", "text": "Cuantos acreedores diferentes tienes?",
             "options": [
                 {"label": "1-2", "value": "few", "score": 1},
                 {"label": "3-5", "value": "mid", "score": 3},
                 {"label": "Mas de 5", "value": "many", "score": 5},
             ], "weight": 1.0},
            {"type": "free_text", "text": "Describe brevemente tu situacion actual", "options": [], "weight": 0},
        ],
        "results": [
            {"label": "No apto por ahora", "min_score": 0, "max_score": 8,
             "message": "Tu situacion actual no cumple los requisitos minimos para acogerte a la ley de insolvencia.",
             "cta_text": "Agenda una asesoria gratuita para explorar otras opciones"},
            {"label": "Apto - requiere revision", "min_score": 8.01, "max_score": 25,
             "message": "Es probable que puedas acogerte a la ley de insolvencia. Se recomienda revision con un abogado.",
             "cta_text": "Programa tu consulta gratuita"},
        ],
    },
    "psicologo_diagnostico": {
        "title": "Evaluacion inicial de bienestar emocional",
        "industry": "salud_mental",
        "language": "es",
        "questions": [
            {"type": "scale", "text": "Como calificarias tu nivel de estres en las ultimas 2 semanas (1-5)?", "options": [], "weight": 1.5},
            {"type": "yes_no", "text": "Has tenido dificultad para dormir recientemente?",
             "options": [{"label": "Si", "value": "yes", "score": 2}, {"label": "No", "value": "no", "score": 0}], "weight": 1.0},
            {"type": "scale", "text": "Que tan motivado te sientes en tu dia a dia (1-5)?", "options": [], "weight": 1.0},
            {"type": "yes_no", "text": "Sientes que necesitas apoyo profesional en este momento?",
             "options": [{"label": "Si", "value": "yes", "score": 3}, {"label": "No", "value": "no", "score": 0}], "weight": 1.0},
            {"type": "free_text", "text": "Que es lo que mas te preocupa actualmente?", "options": [], "weight": 0},
        ],
        "results": [
            {"label": "Bienestar estable", "min_score": 0, "max_score": 4,
             "message": "Tus respuestas indican un buen nivel de bienestar general.",
             "cta_text": "Agenda una sesion de mantenimiento preventivo"},
            {"label": "Recomendado buscar apoyo", "min_score": 4.01, "max_score": 15,
             "message": "Tus respuestas sugieren que podrias beneficiarte de acompanamiento profesional.",
             "cta_text": "Reserva tu primera sesion"},
        ],
    },
    "ecommerce_recomendacion": {
        "title": "Encuentra el producto ideal para ti",
        "industry": "ecommerce",
        "language": "es",
        "questions": [
            {"type": "multiple_choice", "text": "Cual es tu presupuesto aproximado?",
             "options": [
                 {"label": "Menos de $50", "value": "low", "score": 1},
                 {"label": "$50-$150", "value": "mid", "score": 2},
                 {"label": "Mas de $150", "value": "high", "score": 3},
             ], "weight": 1.0},
            {"type": "multiple_choice", "text": "Que buscas principalmente?",
             "options": [
                 {"label": "Calidad", "value": "quality", "score": 3},
                 {"label": "Precio", "value": "price", "score": 1},
                 {"label": "Diseno", "value": "design", "score": 2},
             ], "weight": 1.0},
            {"type": "yes_no", "text": "Es tu primera compra con nosotros?",
             "options": [{"label": "Si", "value": "yes", "score": 1}, {"label": "No", "value": "no", "score": 2}], "weight": 1.0},
        ],
        "results": [
            {"label": "Plan basico", "min_score": 0, "max_score": 4,
             "message": "Te recomendamos nuestra linea basica, excelente relacion precio-calidad.",
             "cta_text": "Ver productos recomendados"},
            {"label": "Plan premium", "min_score": 4.01, "max_score": 10,
             "message": "Te recomendamos nuestra linea premium.",
             "cta_text": "Ver productos premium"},
        ],
    },
}
