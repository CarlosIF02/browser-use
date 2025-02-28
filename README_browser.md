# browser.py
```py
class BrowserConfig:
	r"""
	Configuration for the Browser.

	Default values:
		headless: True
			Whether to run browser in headless mode

		disable_security: True
			Disable browser security features

		extra_chromium_args: []
			Extra arguments to pass to the browser

		wss_url: None
			Connect to a browser instance via WebSocket

		cdp_url: None
			Connect to a browser instance via CDP

		chrome_instance_path: None
			Path to a Chrome instance to use to connect to your normal browser
			e.g. '/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome'
	"""

	headless: bool = False
	disable_security: bool = True
	extra_chromium_args: list[str] = field(default_factory=list)
	chrome_instance_path: str | None = None
	wss_url: str | None = None
	cdp_url: str | None = None

	proxy: ProxySettings | None = field(default=None)
	new_context_config: BrowserContextConfig = field(default_factory=BrowserContextConfig)

	_force_keep_browser_alive: bool = False
```
###### 
- With new_context_config we can set up a new browser to save docs and use cookies files.
- Sceenshots on region Browser Actions
- Region user Actions , actions that the agent can do to navigate



###### 

# context.py Documentation

This module enhances the Playwright browser with additional functionalities and configurations. It provides a `BrowserContext` class that manages browser sessions, handles navigation, and interacts with web pages.

## Key Classes

### BrowserContextConfig

This class holds the configuration for the `BrowserContext`. It includes various settings such as cookies file path, security settings, wait times, browser window size, and more.

#### Attributes:
- `cookies_file`: Path to cookies file for persistence.
- `minimum_wait_page_load_time`: Minimum time to wait before getting page state.
- `wait_for_network_idle_page_load_time`: Time to wait for network requests to finish.
- `maximum_wait_page_load_time`: Maximum time to wait for page load.
- `wait_between_actions`: Time to wait between actions.
- `disable_security`: Disable browser security features.
- `browser_window_size`: Default browser window size.
- `no_viewport`: Disable viewport.
- `save_recording_path`: Path to save video recordings.
- `save_downloads_path`: Path to save downloads.
- `trace_path`: Path to save trace files.
- `locale`: Specify user locale.
- `user_agent`: Custom user agent to use.
- `highlight_elements`: Highlight elements in the DOM.
- `viewport_expansion`: Viewport expansion in pixels.
- `allowed_domains`: List of allowed domains that can be accessed.
- `include_dynamic_attributes`: Include dynamic attributes in the CSS selector.
- `_force_keep_context_alive`: Force keep context alive.

### BrowserSession

This class represents a browser session, holding the context, current page, and cached state.

#### Attributes:
- `context`: The Playwright browser context.
- `current_page`: The current page in the browser.
- `cached_state`: The cached state of the browser.

### BrowserContext

This class manages the browser context, handling initialization, navigation, and interactions with web pages.

#### Methods:
- `__init__(self, browser, config)`: Initializes the browser context.
- `__aenter__(self)`: Async context manager entry.
- `__aexit__(self, exc_type, exc_val, exc_tb)`: Async context manager exit.
- `close(self)`: Closes the browser instance.
- `_initialize_session(self)`: Initializes the browser session.
- `_add_new_page_listener(self, context)`: Adds a listener for new pages.
- `get_session(self)`: Lazy initialization of the browser and related components.
- `get_current_page(self)`: Gets the current page.
- `_create_context(self, browser)`: Creates a new browser context with anti-detection measures.
- `_wait_for_stable_network(self)`: Waits for the network to stabilize.
- `_wait_for_page_and_frames_load(self, timeout_overwrite)`: Ensures the page is fully loaded.
- `_is_url_allowed(self, url)`: Checks if a URL is allowed based on the whitelist configuration.
- `_check_and_handle_navigation(self, page)`: Checks if the current page URL is allowed and handles it if not.
- `navigate_to(self, url)`: Navigates to a URL.
- `refresh_page(self)`: Refreshes the current page.
- `go_back(self)`: Navigates back in history.
- `go_forward(self)`: Navigates forward in history.
- `close_current_tab(self)`: Closes the current tab.
- `get_page_html(self)`: Gets the current page HTML content.
- `execute_javascript(self, script)`: Executes JavaScript code on the page.
- `get_state(self)`: Gets the current state of the browser.
- `_update_state(self, focus_element)`: Updates and returns the state.
- `take_screenshot(self, full_page)`: Takes a screenshot of the current page.
- `remove_highlights(self)`: Removes all highlight overlays and labels.
- `get_tabs_info(self)`: Gets information about all tabs.
- `switch_to_tab(self, page_id)`: Switches to a specific tab by its page_id.
- `create_new_tab(self, url)`: Creates a new tab and optionally navigates to a URL.
- `get_selector_map(self)`: Gets the selector map.
- `get_element_by_index(self, index)`: Gets an element by its index.
- `get_dom_element_by_index(self, index)`: Gets a DOM element by its index.
- `save_cookies(self)`: Saves current cookies to file.
- `is_file_uploader(self, element_node, max_depth, current_depth)`: Checks if an element or its children are file uploaders.
- `get_scroll_info(self, page)`: Gets scroll position information for the current page.
- `reset_context(self)`: Resets the browser session.
- `_get_initial_state(self, page)`: Gets the initial state of the browser.
- `_get_unique_filename(self, directory, filename)`: Generates a unique filename.

## Usage

To use the `BrowserContext`, create an instance with the desired configuration and use it within an async context manager:

```python
from browser_use.browser.context import BrowserContext, BrowserContextConfig

config = BrowserContextConfig(
    cookies_file='path/to/cookies.json',
    allowed_domains=['example.com'],
    # ... other configurations ...
)

async with BrowserContext(browser, config) as context:
    await context.navigate_to('https://example.com')
    html = await context.get_page_html()
    print(html)




Documentación del Código del Agente de Navegación Automatizada

Descripción General

Este código define una clase Agent que permite la automatización de interacciones con un navegador web mediante modelos de lenguaje (LLMs). Está diseñado para ejecutar tareas en una página web, manejar acciones, gestionar estados del navegador y almacenar historiales de ejecución. Se apoya en el uso de Playwright y LangChain para facilitar la interacción con el navegador y la toma de decisiones basada en IA.

Dependencias Principales

El código importa varias librerías y módulos, incluyendo:

asyncio: Para ejecutar operaciones asíncronas.

json, re, logging: Para manejar logs, datos estructurados y expresiones regulares.

dotenv: Para cargar variables de entorno.

pydantic: Para validación de datos.

langchain_core.language_models.chat_models: Para la integración con modelos de lenguaje.

browser_use: Conjunto de módulos internos que manejan la interacción con el navegador.

Clase Agent

Propósito

La clase Agent permite la ejecución de tareas automatizadas en un navegador mediante el uso de modelos de lenguaje. Se encarga de:

Administrar una sesión de navegador.

Ejecutar acciones en una página web.

Almacenar el historial de interacciones.

Manejar errores y reintentos.

Inicialización

agent = Agent(
    task="Descripción de la tarea a realizar",
    llm=ChatOpenAI(),
    browser=Browser(),
    use_vision=True,
    max_actions_per_step=10,
)

Parámetros Principales

task: (str) Descripción de la tarea que el agente debe realizar.

llm: (BaseChatModel) Modelo de lenguaje utilizado para interpretar acciones.

browser: (Browser | None) Instancia del navegador automatizado.

use_vision: (bool) Indica si el agente debe usar análisis visual para la toma de decisiones.

max_actions_per_step: (int) Número máximo de acciones que el agente puede ejecutar por paso.

Métodos Clave

log_response(response: AgentOutput) -> None

Registra el estado actual del agente, incluyendo el resumen de la página, la evaluación del objetivo anterior y las próximas acciones a tomar.

step(self, step_info: Optional[AgentStepInfo] = None) -> None

Ejecuta un paso de la tarea automatizada, obteniendo el estado actual de la página y determinando la siguiente acción a realizar.

run(self, max_steps: int = 100) -> AgentHistoryList

Ejecuta la tarea completa con un máximo de max_steps pasos. Finaliza si el agente alcanza su objetivo o si ocurre un error.

take_step(self) -> tuple[bool, bool]

Ejecuta un único paso y devuelve una tupla indicando si la tarea se completó y si la salida es válida.

multi_act(self, actions: list[ActionModel], check_for_new_elements: bool = True) -> list[ActionResult]

Ejecuta múltiples acciones en la página y devuelve una lista con los resultados de cada acción.

set_tool_calling_method(self, tool_calling_method: Optional[ToolCallingMethod]) -> Optional[ToolCallingMethod]

Determina qué método de llamada de herramientas debe utilizar el agente en función del modelo de lenguaje empleado.

save_history(self, file_path: Optional[str | Path] = None) -> None

Guarda el historial de acciones en un archivo JSON.

rerun_history(self, history: AgentHistoryList, max_retries: int = 3, skip_failures: bool = True, delay_between_actions: float = 2.0) -> list[ActionResult]

Repite la ejecución de una secuencia de acciones basándose en un historial previo.

Manejo de Errores y Validaciones

handle_step_error(self, error: Exception) -> list[ActionResult]

Maneja errores que pueden ocurrir durante la ejecución de un paso. Identifica problemas comunes como fallos en la validación de datos o restricciones de tokens en el modelo de lenguaje.

_validate_output(self) -> bool

Evalúa si la salida generada por el agente es válida con respecto a la tarea solicitada.

Integración con Telemetría

El agente captura eventos de telemetría para registrar información sobre el rendimiento y éxito de las ejecuciones. Ejemplo:

self.telemetry.capture(
    AgentRunTelemetryEvent(
        agent_id=self.state.agent_id,
        task=self.task,
        model_name=self.model_name,
        success=self.state.history.is_done(),
    )
)

Conclusión

Este código proporciona un marco flexible y extensible para la automatización de interacciones web mediante IA. Su arquitectura modular permite integraciones con diferentes modelos de lenguaje y navegadores, facilitando su aplicación en distintos casos de uso, como la extracción de datos, automatización de formularios y pruebas automatizadas.
```