import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from app.utils.constants import PROMPT_SYSTEM_TEXT


async def send_to_llm_agent(user_message: str) -> str:
    """
    Isolated core utility executing physical outbound API payloads to the OpenAI gateway.
    Targeted inside integration test runners to decouple networking pipelines cleanly.
    """
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.2,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", PROMPT_SYSTEM_TEXT),
        ("human", "{input}")
    ])

    chain = prompt | llm
    response = await chain.ainvoke({"input": user_message})
    return str(response.content)
