# Manual Azure Deployment Steps (No Azure CLI Required)

If you're having issues installing Azure CLI, follow these manual steps using the Azure Portal:

## Step 1: Create Azure Resources in Portal

1. Go to https://portal.azure.com
2. Log in with your Microsoft account

### Create a Resource Group
- Click "Create a resource" > Search "Resource Group"
- Name: `smart-retail-rg`
- Region: `East US`
- Click "Review + Create" > "Create"

### Create App Service Plan
- Click "Create a resource" > Search "App Service Plan"
- Name: `smart-retail-plan`
- Operating System: `Linux`
- Sku and size: `B2` (Basic tier, ~$50/month)
- Click "Review + Create" > "Create"

### Create Web App
- Click "Create a resource" > Search "Web App"
- Name: `smart-retail-app` (must be globally unique)
- Publish: `Code`
- Runtime stack: `Python 3.11`
- App Service Plan: select `smart-retail-plan`
- Click "Review + Create" > "Create"

## Step 2: Configure Deployment

### Set Up Git Deployment
1. In your Web App > Deployment Center
2. Source: Select `Local Git`
3. Click "Save"
4. You'll see a Git Clone URL (copy this)

### Add Azure Git Remote Locally
In your PowerShell terminal:
```powershell
cd d:\Smart\ Retail\ Assistant

# Add the Azure remote (replace with URL from step above)
git remote add azure <YOUR-CLONE-URL-FROM-PORTAL>

# Deploy your code
git push azure main
```

## Step 3: Configure Environment Variables

1. In your Web App > Configuration > Application settings
2. Add these variables (click "New application setting"):

| Name | Value |
|------|-------|
| `MONGO_URI` | Your MongoDB connection string |
| `AZURE_OPENAI_API_KEY` | Your Azure OpenAI API key |
| `AZURE_OPENAI_ENDPOINT` | https://your-resource.openai.azure.com/ |
| `AZURE_OPENAI_DEPLOYMENT` | gpt-4o-mini |
| `AZURE_OPENAI_API_VERSION` | 2024-03-01-preview |
| `AZURE_OPENAI_EMBEDDING_DEPLOYMENT` | text-embedding-3-small |
| `DATABASE_NAME` | smart_retail_db |

3. Click "Save"

## Step 4: Monitor Deployment

1. In your Web App > Deployment Center > Logs
2. Wait for build to complete (may take 5-10 minutes)
3. Check Web App > General Properties for the URL

## Step 5: Test Your App

Once deployment completes:
- API: https://smart-retail-app.azurewebsites.net/
- Docs: https://smart-retail-app.azurewebsites.net/docs

### Monitor Logs
1. Web App > App Service logs (enable if needed)
2. Web App > Log stream to view real-time logs

---

## Troubleshooting

### Build fails
- Check Application Insight or Deployment logs for errors
- Common issues: Missing environment variables, Python version mismatch

### Can't connect to MongoDB
- Check your `MONGO_URI` is correct
- MongoDB Atlas: Go to Network Access > Add Azure datacenter IP

### 500 errors
- Check Web App > Log stream for error details
- Verify all environment variables are set correctly

---

**Still prefer command-line?** Try installing Azure CLI manually:

```powershell
# Download and run installer
$ProgressPreference = 'SilentlyContinue'
Invoke-WebRequest -Uri https://aka.ms/installazurecliwindows -OutFile AzureCLI.msi
msiexec /I AzureCLI.msi /passive
Remove-Item AzureCLI.msi

# Then close and reopen PowerShell, then run:
az login
.\deploy-to-azure.ps1
```
