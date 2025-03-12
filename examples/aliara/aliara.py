import asyncio
import os
import json
import nest_asyncio
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import AzureChatOpenAI
from browser_use import Agent
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContextConfig

# Configuración para Jupyter (no necesaria en script, pero no hace daño)
nest_asyncio.apply()

# Cargar variables de entorno
load_dotenv()

# Configurar LLM (Langchain con Azure OpenAI)
llm = AzureChatOpenAI(
    max_tokens=5000,
    temperature=0,
    max_retries=20,
    request_timeout=500,
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_deployment=os.getenv("AZURE_OPENAI_CHAT_VERSION"),
)

# Tarea a ejecutar
task = """
Acepta las cookies siempre como primer paso.

Entra en https://ov.aliaraenergia.es/login?

Tienes que utilizar las credenciales siguientes:
-Usuario: x_name
-Contraseña: x_password

Como el primer paso acepta las cookies de Google, tienes que aceptarlas todas.

Descarga el excel de mis movimientos 
"""

# Modelo Pydantic para la salida
class DownloadURL(BaseModel):
    download_link: str

# Configuración del navegador
context_config = BrowserContextConfig(
    save_downloads_path="/mnt/c/Users/civars_bec/Downloads",
    # browser_window_size={"width": 2000, "height": 1100},
)

config = BrowserConfig(
    headless=False,  # Cambiar a True si quieres que sea en segundo plano
    new_context_config=context_config,
    chrome_instance_path="/usr/bin/google-chrome"  # Linux
)

# Credenciales
sensitive_data = {
    'x_name': os.getenv("ALIARA_USER"),
    'x_password': os.getenv("ALIARA_PASSWORD")
}

# Crear navegador
browser = Browser(config=config)

# Función principal
async def main():
    agent = Agent(
        task=task,
        llm=llm,
        sensitive_data=sensitive_data,
        max_actions_per_step=8,
        use_vision=True,
        browser=browser,
        save_conversation_path="/mnt/c/Users/civars_bec/Downloads",
    )

    # Ejecutar agente
   # history = await agent.run()
   # result = history.final_result()
    result = True
    if result:
        try:
            #parsed = json.loads(result)
            download_url ="https://ov.aliaraenergia.es/mis-movimientos/exportar-excel"# parsed.get("download_link", None)
            if download_url:
                print(f'🔗 URL de descarga detectada: {download_url}')
            else:
                print(" No se encontró la URL de descarga en la respuesta.")
        except json.JSONDecodeError:
            print(f"Error: La respuesta no es un JSON válido: {result}")

    # Crear segundo agente para descargar el archivo
    download_agent = Agent(
        task=f"Accede a esta URL para que se inicie la descarga automaticamente {download_url}",
        llm=llm,
        browser=browser,
        sensitive_data=sensitive_data,
    )

    await download_agent.run()

    # Cerrar el navegador al finalizar
    await browser.close()
   

# Ejecutar la función principal solo si se ejecuta este script directamente
if __name__ == "__main__":
    asyncio.run(main())