import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from fpdf import FPDF
import streamlit as st

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    api_key = st.secrets["OPENAI_API_KEY"]

client = OpenAI(api_key=api_key)


def validate_inputs(data: dict) -> list:
    errors = []

    required_fields = [
        "business_name",
        "niche",
        "product_service",
        "target_audience",
    ]

    for field in required_fields:
        if not data.get(field, "").strip():
            errors.append(f"{field.replace('_', ' ').title()} is required.")

    return errors


def generate_marketing_content(prompt: str, model: str = "gpt-4o-mini") -> dict:
    response = client.responses.create(
        model=model,
        input=prompt
    )

    raw_text = response.output_text.strip()

    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        start = raw_text.find("{")
        end = raw_text.rfind("}") + 1

        if start != -1 and end != -1:
            possible_json = raw_text[start:end]
            try:
                return json.loads(possible_json)
            except json.JSONDecodeError:
                pass

        raise ValueError("The AI response was not valid JSON.")


def format_result_as_text(result: dict) -> str:
    lines = []

    lines.append("AI Marketing Content Agent Output")
    lines.append("=" * 40)
    lines.append("")

    lines.append("BUSINESS SUMMARY")
    lines.append(result["business_summary"])
    lines.append("")

    lines.append("BLOG IDEAS")
    for i, idea in enumerate(result["blog_ideas"], start=1):
        lines.append(f"{i}. {idea}")
    lines.append("")

    lines.append("SEO TITLES")
    for i, title in enumerate(result["seo_titles"], start=1):
        lines.append(f"{i}. {title}")
    lines.append("")

    lines.append("META DESCRIPTIONS")
    for i, desc in enumerate(result["meta_descriptions"], start=1):
        lines.append(f"{i}. {desc}")
    lines.append("")

    lines.append("SOCIAL MEDIA CAPTIONS")
    for i, caption in enumerate(result["social_captions"], start=1):
        lines.append(f"{i}. {caption}")
    lines.append("")

    lines.append("LANDING PAGE HERO SECTION")
    lines.append(f"Headline: {result['landing_page']['headline']}")
    lines.append(f"Subheadline: {result['landing_page']['subheadline']}")
    lines.append(f"CTA: {result['landing_page']['cta']}")
    lines.append("")

    return "\n".join(lines)


def sanitize_pdf_text(text: str) -> str:
    replacements = {
        "–": "-",
        "—": "-",
        "“": '"',
        "”": '"',
        "‘": "'",
        "’": "'",
        "…": "...",
        "\u00a0": " ",
        "•": "-",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    cleaned = []
    for ch in text:
        code = ord(ch)

        if 32 <= code <= 126 or ch in "\n\r\t":
            cleaned.append(ch)

    return "".join(cleaned)

def contains_arabic(text: str) -> bool:
    for ch in text:
        if '\u0600' <= ch <= '\u06FF':
            return True
    return False


def format_result_as_pdf(result: dict) -> bytes:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(
        0,
        10,
        sanitize_pdf_text("AI Marketing Content Agent Output"),
        new_x="LMARGIN",
        new_y="NEXT"
    )
    pdf.ln(2)

    def add_section_title(title: str):
        pdf.set_font("Helvetica", "B", 13)
        pdf.cell(
            0,
            10,
            sanitize_pdf_text(title),
            new_x="LMARGIN",
            new_y="NEXT"
        )
        pdf.set_font("Helvetica", size=11)

    def add_paragraph(text: str):
        pdf.multi_cell(0, 7, sanitize_pdf_text(text))
        pdf.ln(1)

    add_section_title("Business Summary")
    add_paragraph(result["business_summary"])

    add_section_title("Blog Ideas")
    for i, idea in enumerate(result["blog_ideas"], start=1):
        add_paragraph(f"{i}. {idea}")

    add_section_title("SEO Titles")
    for i, title in enumerate(result["seo_titles"], start=1):
        add_paragraph(f"{i}. {title}")

    add_section_title("Meta Descriptions")
    for i, desc in enumerate(result["meta_descriptions"], start=1):
        add_paragraph(f"{i}. {desc}")

    add_section_title("Social Media Captions")
    for i, caption in enumerate(result["social_captions"], start=1):
        add_paragraph(f"{i}. {caption}")

    add_section_title("Landing Page Hero Section")
    add_paragraph(f"Headline: {result['landing_page']['headline']}")
    add_paragraph(f"Subheadline: {result['landing_page']['subheadline']}")
    add_paragraph(f"CTA: {result['landing_page']['cta']}")

    return bytes(pdf.output())
