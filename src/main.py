import os
from pathlib import Path
from dotenv import load_dotenv

from load_data import load_json, load_text
from llm_tailor import tailor_cv


def main():
    load_dotenv()

    profile = load_json("data/profile_master.json")
    job_text = load_text("jobs/sample_job.txt")
    prompt = load_text("prompts/tailor_cv_prompt.txt")

    result = tailor_cv(profile, job_text, prompt)

    output_path = Path("output/tailored_cv.md")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(result, encoding="utf-8")

    print(f"Saved tailored CV to: {output_path}")


if __name__ == "__main__":
    main()