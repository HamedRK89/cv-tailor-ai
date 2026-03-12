'''
import json
import os
from openai import OpenAI


def tailor_cv(profile: dict, job_text: str, system_prompt: str) -> dict:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    user_message = f"""
    Candidate profile JSON:
    {json.dumps(profile, indent=2)}

    Job description:
    {job_text}
    """

    response = client.responses.create(
        model="gpt-5-mini",
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        max_output_tokens=1200,
    )

    raw_text = response.output_text.strip()

    try:
        return json.loads(raw_text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Model did not return valid JSON. Output was:\\n{raw_text}") from e
'''
import json
import os
from openai import OpenAI


CV_SCHEMA = {
    "type": "object",
    "properties": {
        "professional_summary": {"type": "string"},
        "selected_skills": {
            "type": "array",
            "items": {"type": "string"}
        },
        "relevant_experience": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "role": {"type": "string"},
                    "organization": {"type": "string"},
                    "bullets": {
                        "type": "array",
                        "items": {"type": "string"}
                    }
                },
                "required": ["role", "organization", "bullets"],
                "additionalProperties": False
            }
        },
        "relevant_projects": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "bullets": {
                        "type": "array",
                        "items": {"type": "string"}
                    }
                },
                "required": ["name", "bullets"],
                "additionalProperties": False
            }
        },
        "notes": {
            "type": "object",
            "properties": {
                "strong_matches": {
                    "type": "array",
                    "items": {"type": "string"}
                },
                "partial_matches": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            },
            "required": ["strong_matches", "partial_matches"],
            "additionalProperties": False
        }
    },
    "required": [
        "professional_summary",
        "selected_skills",
        "relevant_experience",
        "relevant_projects",
        "notes"
    ],
    "additionalProperties": False
}


def tailor_cv(profile: dict, job_text: str, system_prompt: str) -> dict:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    user_message = f"""
    Candidate profile JSON:
    {json.dumps(profile, indent=2)}

    Job description:
    {job_text}
    """

    response = client.responses.create(
        model="gpt-5-mini",
        instructions=system_prompt,
        input=user_message,
        text={
            "format": {
                "type": "json_schema",
                "name": "tailored_cv",
                "schema": CV_SCHEMA,
                "strict": True
            }
        },
        max_output_tokens=3000,
    )

    # Primary path: structured text content
    raw_text = (response.output_text or "").strip()

    if not raw_text:
        # Helpful debug if something unexpected happens
        raise ValueError(
            f"Model returned empty output_text. Full response object:\n{response.model_dump_json(indent=2)}"
        )
    print("RAW OUTPUT START")
    print(raw_text)
    print("RAW OUTPUT END")
    print("RAW OUTPUT LENGTH:", len(raw_text))

    return json.loads(raw_text)