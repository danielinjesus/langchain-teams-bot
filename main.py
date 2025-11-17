# FastAPI 기반 / # 실행 uvicorn main:app --reload / # Bot Framework 추가
from dotenv import load_dotenv; import os
from types import SimpleNamespace
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from langchain_openai import AzureChatOpenAI
from pydantic import BaseModel
from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import Activity
from botbuilder.integration.aiohttp import CloudAdapter, ConfigurationBotFrameworkAuthentication

load_dotenv(override=True)

# Minimal LLM setup
llm = AzureChatOpenAI(
    api_key=os.getenv('AZURE_OPENAI_API_KEY'),
    azure_endpoint=os.getenv('END_POINT'),
    azure_deployment=os.getenv('MODEL_NAME'),
    api_version=os.getenv('api_version') )

# Bot Framework Configuration
bot_config = SimpleNamespace(
    APP_ID=os.getenv('MicrosoftAppId'),
    APP_PASSWORD=os.getenv('MicrosoftAppPassword'),
    APP_TYPE=os.getenv('MicrosoftAppType'),
    APP_TENANTID=os.getenv('MicrosoftAppTenantId')
)
auth = ConfigurationBotFrameworkAuthentication(bot_config)
adapter = CloudAdapter(auth)

# Bot Class
class LLMBot(ActivityHandler):
    async def on_message_activity(self, turn_context: TurnContext):
        user_message = turn_context.activity.text.strip()
        if user_message:
            bot_response = await llm.ainvoke(user_message)
            await turn_context.send_activity(str(bot_response.content))

bot = LLMBot()

app = FastAPI(title="Azure Chat API", version="1.0")

# CORS middleware for Azure Bot Service
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class ChatRequest(BaseModel):
    input: str

class ChatResponse(BaseModel):
    output: str

@app.get("/")
def root():
    return {"status": "running"}

@app.post("/chat")
def chat(request: ChatRequest):
    response = llm.invoke(request.input)
    return ChatResponse(output=response.content)

# Bot Framework endpoint for Teams
@app.post("/api/messages")
async def messages(req: Request):
    return await adapter.process(req, bot)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
