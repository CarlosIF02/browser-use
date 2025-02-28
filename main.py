from langchain_openai import ChatOpenAI
from browser_use import Agent
import asyncio
from dotenv import load_dotenv
from langchain_openai import AzureOpenAI, AzureChatOpenAI
import os
# Cargar variables de entorno
load_dotenv()

async def main():
    agent = Agent(
        task="""Entra en la url https://boc.cantabria.es/boces/. 
        
        Busca por BOC de fecha filtro accede al dia 5 de febrero de 2025.

        ¿Hay algun link a documentos?

        extrae en formato texto el href de los link

        """,
        llm = AzureChatOpenAI(
            max_tokens=5000,
            temperature=0,
            max_retries=20,
            request_timeout=500,
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            azure_deployment=os.getenv("AZURE_OPENAI_CHAT_VERSION"),
            ),
    )
    result = await agent.run()
    print(result)

# Ejecutar el agente
asyncio.run(main())
