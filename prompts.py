def build_marketing_prompt(
    business_name: str,
    niche: str,
    product_service: str,
    target_audience: str,
    country: str,
    language: str,
    tone: str,
    platform: str,
) -> str:
    return f"""
You are an expert digital marketing strategist, SEO specialist, and copywriter.

Generate high-quality marketing content for a business based on the details below.

Business details:
- Business Name: {business_name}
- Niche / Industry: {niche}
- Product or Service: {product_service}
- Target Audience: {target_audience}
- Country / Market: {country}
- Language: {language}
- Tone of Voice: {tone}
- Platform: {platform}

Rules:
- Make the content specific to the niche and target audience.
- Do not write generic marketing copy.
- Match the requested tone and language.
- Keep SEO titles clear and clickable.
- Keep meta descriptions concise and practical.
- Social captions should feel natural and platform-appropriate.
- Landing page copy should be persuasive and clear.
- Do not use emojis or decorative symbols.
- Return valid JSON only.
- Do not add explanations outside the JSON.

Return this exact structure:
{{
  "business_summary": "A short summary of the business, audience, and marketing direction.",
  "blog_ideas": [
    "Idea 1",
    "Idea 2",
    "Idea 3",
    "Idea 4",
    "Idea 5"
  ],
  "seo_titles": [
    "Title 1",
    "Title 2",
    "Title 3"
  ],
  "meta_descriptions": [
    "Description 1",
    "Description 2",
    "Description 3"
  ],
  "social_captions": [
    "Caption 1",
    "Caption 2",
    "Caption 3"
  ],
  "landing_page": {{
    "headline": "Headline text",
    "subheadline": "Subheadline text",
    "cta": "CTA text"
  }}
}}
"""
