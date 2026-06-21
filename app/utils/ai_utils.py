import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from app.utils.constants import PROMPT_SYSTEM_TEXT


async def send_to_llm_agent(user_message: str) -> str:
    """
    Core utility executing physical outbound API payloads to the Google Gemini gateway.
    Uses the free tier API token stored inside your local .env configuration.
    """
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.2,
        google_api_key=os.getenv("OPENAI_API_KEY")
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", PROMPT_SYSTEM_TEXT),
        ("human", "{input}")
    ])

    chain = prompt | llm
    response = await chain.ainvoke({"input": user_message})
    return str(response.content)
