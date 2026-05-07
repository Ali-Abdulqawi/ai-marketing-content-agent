# AI Marketing Content Agent

An AI-powered Streamlit web app that generates marketing content for businesses, including blog ideas, SEO titles, meta descriptions, social media captions, and landing page copy.

## Live Demo
[Try the app here](https://ai-marketing-content-agent.streamlit.app/)

## GitHub Repository
[View the source code](https://github.com/Ali-Abdulqawi/ai-marketing-content-agent)

---

## Overview

The AI Marketing Content Agent helps businesses quickly generate tailored marketing content based on their niche, target audience, market, language, tone of voice, and platform.

This project was built as a practical MVP to demonstrate how AI can streamline content creation and support marketing workflows.

---

## Features

- Generate a short business summary
- Generate blog content ideas
- Generate SEO-friendly titles
- Generate meta descriptions
- Generate social media captions
- Generate landing page hero copy
- Support for English and Arabic content
- Download results as TXT
- Download results as PDF (English output)
- Clean Streamlit-based interface
- Cloud deployment with Streamlit Community Cloud

---

## Tech Stack

- **Python**
- **Streamlit**
- **OpenAI API**
- **python-dotenv**
- **fpdf2**

---

## How It Works

Users enter:
- Business name
- Niche / industry
- Product or service
- Target audience
- Country / market
- Language
- Tone of voice
- Platform

The app then uses the OpenAI API to generate structured marketing content and displays the results in an easy-to-copy format.

---

## Project Structure

```bash
ai-marketing-content-agent/
├── app.py
├── prompts.py
├── utils.py
├── requirements.txt
└── .gitignore
