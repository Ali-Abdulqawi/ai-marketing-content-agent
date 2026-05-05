import streamlit as st
from prompts import build_marketing_prompt
from utils import (
    validate_inputs,
    generate_marketing_content,
    format_result_as_text,
    format_result_as_pdf,
    contains_arabic,
)

if "result" not in st.session_state:
    st.session_state.result = None

if "export_text" not in st.session_state:
    st.session_state.export_text = None

if "export_pdf" not in st.session_state:
    st.session_state.export_pdf = None
st.set_page_config(page_title="AI Marketing Content Agent", layout="wide")

st.sidebar.title("About")
st.sidebar.info(
    "This AI Marketing Content Agent generates blog ideas, SEO titles, "
    "meta descriptions, social media captions, and landing page copy."
)

st.sidebar.subheader("How to use")
st.sidebar.write(
    """
    1. Enter business details  
    2. Choose language, tone, and platform  
    3. Click Generate Content  
    4. Download the result as TXT or PDF
    """
)
st.title("AI Marketing Content Agent")
st.write("Generate blog ideas, SEO titles, meta descriptions, social captions, and landing page copy.")

with st.form("marketing_form"):
    business_name = st.text_input("Business Name")
    niche = st.text_input("Niche / Industry")
    product_service = st.text_input("Product or Service")
    target_audience = st.text_area("Target Audience")
    country = st.text_input("Country / Market")

    language = st.selectbox("Language", ["English", "Arabic"])
    tone = st.selectbox(
        "Tone of Voice",
        ["Professional", "Friendly", "Luxury", "Casual", "Persuasive"]
    )
    platform = st.selectbox(
        "Platform",
        ["Website", "Instagram", "Facebook", "LinkedIn", "Blog", "Google Ads"]
    )

    submitted = st.form_submit_button("Generate Content")

if submitted:
    form_data = {
        "business_name": business_name,
        "niche": niche,
        "product_service": product_service,
        "target_audience": target_audience,
    }

    errors = validate_inputs(form_data)

    if errors:
        for error in errors:
            st.error(error)
    else:
        prompt = build_marketing_prompt(
            business_name=business_name,
            niche=niche,
            product_service=product_service,
            target_audience=target_audience,
            country=country,
            language=language,
            tone=tone,
            platform=platform,
        )

        try:
            with st.spinner("Generating content..."):
                result = generate_marketing_content(prompt)

            export_text = format_result_as_text(result)
            has_arabic = contains_arabic(export_text)

            export_pdf = None
            if not has_arabic:
                export_pdf = format_result_as_pdf(result)
           
            st.session_state.result = result
            st.session_state.export_text = export_text
            st.session_state.export_pdf = export_pdf

            st.success("Content generated successfully.")

            st.subheader("Business Summary")
            st.text_area("Summary", result["business_summary"], height=120)

            with st.expander("Blog Ideas", expanded=True):
                for i, idea in enumerate(result["blog_ideas"], start=1):
                    st.text_area(f"Blog Idea {i}", idea, height=70)

            with st.expander("SEO Titles", expanded=True):
                for i, title in enumerate(result["seo_titles"], start=1):
                    st.text_area(f"SEO Title {i}", title, height=70)

            with st.expander("Meta Descriptions", expanded=True):
                for i, desc in enumerate(result["meta_descriptions"], start=1):
                    st.text_area(f"Meta Description {i}", desc, height=90)

            with st.expander("Social Media Captions", expanded=True):
                for i, caption in enumerate(result["social_captions"], start=1):
                    st.text_area(f"Caption {i}", caption, height=120)

            st.subheader("Landing Page Hero Section")
            st.text_area("Headline", result["landing_page"]["headline"], height=80)
            st.text_area("Subheadline", result["landing_page"]["subheadline"], height=100)
            st.text_area("CTA", result["landing_page"]["cta"], height=70)
            

            st.download_button(
                label="Download as TXT",
                data=export_text,
                file_name="marketing_content.txt",
                mime="text/plain"
            )
            
            if export_pdf:
                st.download_button(
                    label="Download as PDF",
                    data=export_pdf,
                    file_name="marketing_content.pdf",
                    mime="application/pdf"
                )
            
            else:
                st.info("PDF export is currently available for English output only. Use TXT for Arabic content.")

            if st.button("Clear Results"):
                st.session_state.result = None
                st.session_state.export_text = None
                st.session_state.export_pdf = None
                st.rerun()

        except Exception as e:
            st.error(f"Generation failed: {str(e)}")
