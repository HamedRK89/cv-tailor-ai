import json
import subprocess

from pathlib import Path
from dotenv import load_dotenv

from load_data import load_json, load_text
from llm_tailor import tailor_cv
from latex_renderer import render_template


def compile_latex(tex_path: str, output_dir: str = "output"):
    result = subprocess.run(
        ["pdflatex", "-interaction=nonstopmode", f"-output-directory={output_dir}", tex_path],
        text=True,
        capture_output=True
    )

    print(result.stdout)
    if result.returncode != 0:
        print("LaTeX compilation returned a non-zero exit code.")
        print(result.stderr)

        pdf_path = tex_path.replace(".tex", ".pdf")
        print(f"Check whether a PDF was still generated: {pdf_path}")

def main():
    load_dotenv()

    profile = load_json("data/profile_master.json")
    job_text = load_text("jobs/sample_job.txt")
    prompt = load_text("prompts/tailor_cv_json_prompt.txt")
    template = load_text("templates/cv_template_real.tex")

    tailored = tailor_cv(profile, job_text, prompt)

    output_dir = Path("output")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    job_name = "ai_engineer_vision"
    json_path = output_dir / f"{job_name}.json"
    tex_path = output_dir / f"{job_name}.tex"
    
    #json_path = output_dir / "tailored_cv.json"
    json_path.write_text(json.dumps(tailored, indent=2, ensure_ascii=False), encoding="utf-8")

    tex_content = render_template(template, tailored)
    tex_path = output_dir / "tailored_cv.tex"
    tex_path.write_text(tex_content, encoding="utf-8")

    print(f"Saved JSON to: {json_path}")
    print(f"Saved LaTeX to: {tex_path}")

    compile_latex(str(tex_path), str(output_dir))
    print(f"Compiled PDF in: {output_dir}")

if __name__ == "__main__":
    main()