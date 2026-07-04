"""
Servicio de generacion de tests via LLM con salida estructurada.
Patron: prompt estructurado -> respuesta JSON forzada -> validacion Pydantic -> retry 1 vez si falla.
"""
import json
from openai import OpenAI
from app.config import settings
from app.schemas import OnboardingInput, GeneratedTestSchema

client = OpenAI(api_key=settings.openai_api_key)

SYSTEM_PROMPT = """Eres un generador experto de tests/cuestionarios de negocio.
Debes devolver EXCLUSIVAMENTE un JSON valido que cumpla este esquema:

{
  "title": string,
  "industry": string,
  "language": "es" | "en",
  "questions": [
    {
      "type": "multiple_choice" | "yes_no" | "scale" | "free_text",
      "text": string,
      "options": [{"label": string, "value": string, "score": number}],
      "weight": number
    }
  ],
  "results": [
    {"label": string, "min_score": number, "max_score": number, "message": string, "cta_text": string}
  ]
}

Reglas:
- Genera exactamente el numero de preguntas solicitado.
- Los resultados deben cubrir todo el rango de puntuacion posible sin huecos ni superposiciones.
- Si el tipo es free_text, options debe ser lista vacia.
- No incluyas texto fuera del JSON. No uses markdown ni backticks.
"""


def _build_user_prompt(data: OnboardingInput) -> str:
    return f"""
Profesional: {data.professional_name} ({data.profession})
Industria: {data.industry}
Descripcion del negocio: {data.business_description}
Objetivo del test: {data.test_goal}
Idioma de salida: {data.language}
Numero de preguntas: {data.num_questions}

Genera el test siguiendo exactamente el esquema JSON indicado en las instrucciones del sistema.
"""


def _call_llm(system_prompt: str, user_prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content


def generate_test(data: OnboardingInput) -> GeneratedTestSchema:
    user_prompt = _build_user_prompt(data)
    raw = _call_llm(SYSTEM_PROMPT, user_prompt)
    try:
        parsed = json.loads(raw)
        return GeneratedTestSchema(**parsed)
    except Exception as first_error:
        retry_prompt = (
            user_prompt
            + f"\n\nTu respuesta anterior fallo la validacion: {first_error}. "
              "Corrige el JSON y devuelve UNICAMENTE el JSON valido."
        )
        raw_retry = _call_llm(SYSTEM_PROMPT, retry_prompt)
        parsed_retry = json.loads(raw_retry)
        return GeneratedTestSchema(**parsed_retry)
