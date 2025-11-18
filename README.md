# How to Register a LangChain App into Microsoft Teams

During a "Build Agent with LangChain" project class, a customer employee needed to ship her ERP-connected LangChain app into Teams for easier internal use. With help from Microsoft Support, I got it working.

<img width="739" height="463" alt="langchain-teams-bot" src="https://github.com/user-attachments/assets/625dd732-d99f-42a6-b834-17a824a4afa6" />

## Setup Guide

### 1. Write Agent Code

#### 1.1 Create LangChain App
- Implement your LangChain logic (agents, chains, tools, etc.)

#### 1.2 Add FastAPI to Create API Server
- Add FastAPI to create REST API endpoints

#### 1.3 Add Bot Framework Library to Connect to Teams
- Install: `botbuilder-core`, `botframework-connector`
- Use `ConfigurationBotFrameworkAuthentication` + `CloudAdapter`

### 2. Deploy to Azure App Service

```bash
az webapp up --name your-app-name --resource-group your-rg
```

### 3. Create Azure Bot (App Registration is automatically done)

#### 3.1 Search and Create Azure Bot in Azure Portal
- Go to Azure Portal → Search "Azure Bot" → Create

#### 3.2 Configure App Service Endpoint
- Messaging endpoint: `https://your-app-name.azurewebsites.net/api/messages`

#### 3.3 Add Environment Variables to Azure App Service
```
MicrosoftAppId=<your-app-id>
MicrosoftAppPassword=<your-app-password>
MicrosoftAppTenantId=<your-tenant-id>
MicrosoftAppType=SingleTenant
```

Add these in: Azure Portal → App Service → Configuration → Application settings

#### 3.4 Enable Microsoft Teams Channel
- Azure Bot → Settings → Channels → Enable Microsoft Teams

#### 3.5 Test Bot Connection in "Test in Web Chat"
- Azure Bot → Settings → "Test in Web Chat"
- **Debugging**: Check logs in App Service → Log stream

### 4. Upload to Teams

#### 4.1 Create Manifest Zip Package
1. Copy `teams-manifest-sample/manifest.json-example` to `manifest.json`
2. Update `manifest.json` with your bot ID, app name, and URLs
3. Zip the folder contents: `manifest.json`, `color.png`, `outline.png`

#### 4.2 Upload in Teams Admin Center
**4.2.1** Teams Apps → Manage Apps → Actions → **Upload new app**

**4.2.2** Teams apps → Manage apps → Search with the app name

**4.2.3** Teams Apps → Setup policies → Global → Enable **Upload custom apps**

**4.2.4** Teams Apps → Setup policies → Global → Pinned apps → **Add Apps** → Search for your app name

#### 4.3 Start Chat in Teams
- Check activated app on the left sidebar in Teams and click to start chatting

## Prerequisites

- Python 3.10
- Azure subscription
- Microsoft Teams Admin access
- Azure App Service
- Azure Bot Service
- Azure OpenAI Service

## Project Structure

- `main.py` - Bot application entry point with Bot Framework adapter
- `requirements.txt` - Python dependencies
- `teams-manifest-sample/` - Teams app manifest template to be uploaded at Teams Admin Center after compressing to a .zip file. 
- `.env_sample` - Environment variables template

## License

MIT
