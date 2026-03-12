from typing import List, Dict


def latex_escape(text: str) -> str:
    replacements = {
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def render_skills(skills: List[str]) -> str:
    escaped = [latex_escape(skill) for skill in skills]
    return ", ".join(escaped)


def render_experience(experience):
    blocks = []
    for item in experience:
        role = latex_escape(item["role"])
        org = latex_escape(item["organization"])
        bullets = item.get("bullets", [])

        bullet_text = "\n".join(f"    \\item {latex_escape(b)}" for b in bullets)

        block = f"""\\textbf{{{role}}} \\hfill {org} \\\\
        \\begin{{itemize}}
        {bullet_text}
        \\end{{itemize}}"""
        blocks.append(block)

    return "\n\n".join(blocks)


def render_projects(projects: List[Dict]) -> str:
    blocks = []
    for item in projects:
        name = latex_escape(item["name"])
        bullets = item.get("bullets", [])

        bullet_text = "\n".join(
            [f"\\item {latex_escape(b)}" for b in bullets]
        )

        block = f"""\\textbf{{{name}}}
\\begin{{itemize}}
{bullet_text}
\\end{{itemize}}"""
        blocks.append(block)

    return "\n\n".join(blocks)


def render_template(template: str, tailored: dict) -> str:
    result = template
    result = result.replace(
        "{{PROFILE_SUMMARY}}",
        latex_escape(tailored["professional_summary"])
    )
    result = result.replace(
        "{{SELECTED_SKILLS}}",
        render_skills(tailored["selected_skills"])
    )
    result = result.replace(
        "{{RELEVANT_EXPERIENCE}}",
        render_experience(tailored["relevant_experience"])
    )
    result = result.replace(
        "{{RELEVANT_PROJECTS}}",
        render_projects(tailored["relevant_projects"])
    )
    return result