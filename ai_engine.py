import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from config import GEMINI_API_KEY

# LLM SETUP
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0.4
)

parser = JsonOutputParser()

#  ENRICH
enrich_prompt = PromptTemplate(
    template="""
Analyze this startup:

Name: {name}
Description: {idea}

Return JSON:
{{
  "pain_point": "",
  "automation_idea": ""
}}
""",
    input_variables=["name", "idea"]
)

enrich_chain = enrich_prompt | llm | parser

def enrich_lead(lead):
    try:
        return enrich_chain.invoke({
            "name": lead["name"],
            "idea": lead["idea"]
        })
    except:
        return {"pain_point": "", "automation_idea": ""}

# EMAIL
email_prompt = PromptTemplate(
    template="""
Write a personalized cold email (80-120 words).

Rules:
- Sender: Ayush (AI automation consultant)
- Address: Hi {name} Team
- Use their idea: {idea}
- Pain point: {pain_point}
- Suggest: {automation_idea}
- No fluff, no emojis

Return JSON:
{{
  "generated_email": ""
}}
""",
    input_variables=["name", "idea", "pain_point", "automation_idea"]
)

email_chain = email_prompt | llm | parser

def generate_email(lead):
    try:
        return email_chain.invoke({
            "name": lead["name"],
            "idea": lead["idea"],
            "pain_point": lead.get("pain_point", ""),
            "automation_idea": lead.get("automation_idea", "")
        })
    except:
        return {"generated_email": ""}