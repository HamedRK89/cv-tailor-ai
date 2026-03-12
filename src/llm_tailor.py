import json
import os
from openai import OpenAI


def tailor_cv(profile: dict, job_text: str, system_prompt: str) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    user_message = f"""
                Candidate profile JSON:
                {json.dumps(profile, indent=2)}

                Job description:
                {job_text}
                """

    response = client.responses.create(
        model="gpt-5",
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
    )

    return response.output_text