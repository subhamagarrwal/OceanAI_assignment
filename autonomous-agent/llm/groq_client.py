import json
from groq import Groq
from config.settings import GROQ_API_KEY, MODEL_TC

client = Groq(api_key=GROQ_API_KEY)

def groq_smart(prompt, model=MODEL_TC, temperature=0.1):
    system_prompt = """
    You are a Senior QA lead,
    Output ONLY a valid JSON object.
    Do not include any markdown formatting or conversational text.
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_completion_tokens=4096,
            response_format={"type": "json_object"}
        )
        return response.choices[0].message.content
    except Exception as e:
        return json.dumps({"error": str(e)})
