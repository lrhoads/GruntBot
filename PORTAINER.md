# GruntBot Portainer Deployment Guide

This guide shows you how to deploy GruntBot using Portainer for easy container management.

## Method 1: Using Portainer Stacks (Recommended)

### Step 1: Access Portainer
1. Open your Portainer web interface
2. Navigate to **Stacks** in the left sidebar
3. Click **+ Add stack**

### Step 2: Create the Stack
1. **Name**: `gruntbot`
2. **Build method**: Choose "Git Repository"
3. **Repository URL**: `https://github.com/lrhoads/GruntBot`
4. **Reference**: `refs/heads/main`
5. **Compose path**: `docker-compose.portainer.yml`

### Step 3: Environment Variables
Add these environment variables in the **Environment variables** section:

| Variable | Value |
|----------|--------|
| `DISCORD_TOKEN` | Your Discord bot token |
| `GOOGLE_API_KEY` | Your Google Generative AI API key |

### Step 4: Deploy
1. Click **Deploy the stack**
2. Wait for the build and deployment to complete
3. Your GruntBot should now be running!

## Method 2: Using Portainer App Templates

### Step 1: Add Custom Template
1. Go to **Settings** → **App Templates**
2. Add this URL to **Template URL**: 
   ```
   https://raw.githubusercontent.com/lrhoads/GruntBot/main/portainer-template.json
   ```

### Step 2: Deploy from Template
1. Go to **App Templates**
2. Find "GruntBot Discord Bot"
3. Fill in your API keys
4. Click **Deploy the container**

## Method 3: Manual Container Creation

### Step 1: Create Volume
1. Go to **Volumes** → **Add volume**
2. Name: `gruntbot-data`
3. Click **Create the volume**

### Step 2: Create Container
1. Go to **Containers** → **Add container**
2. **Name**: `gruntbot`
3. **Image**: `gruntbot:latest` (build locally first)
4. **Environment variables**:
   - `DISCORD_TOKEN=your_token_here`
   - `GOOGLE_API_KEY=your_key_here`
5. **Volumes**:
   - Container: `/app/res` → Volume: `gruntbot-data`
6. **Restart policy**: `Unless stopped`
7. Click **Deploy the container**

## Managing GruntBot in Portainer

### View Logs
1. Go to **Containers**
2. Click on `gruntbot`
3. Click **Logs** tab
4. View real-time or historical logs

### Update GruntBot
1. Go to **Stacks** (if using stacks)
2. Click on `gruntbot` stack
3. Click **Editor**
4. Click **Pull and redeploy**

### Monitor Resources
1. Go to **Containers**
2. Click on `gruntbot`
3. View **Stats** tab for CPU/Memory usage

### Manage Profiles
1. Go to **Volumes**
2. Click **Browse** on `gruntbot-data`
3. Navigate to view/edit `profiles.json`

## Backup Configuration

### Backup User Profiles
1. Go to **Volumes** → `gruntbot-data`
2. Click **Browse**
3. Download `profiles.json` file

### Restore Profiles
1. Upload `profiles.json` back to the volume
2. Restart the container

## Troubleshooting

### Deployment Error: "env file not found"
If you get an error like `failed to resolve services environment: env file /data/compose/24/.env not found`, this means:
1. The stack is looking for a `.env` file that doesn't exist in Portainer
2. **Solution**: Make sure you're using `docker-compose.portainer.yml` (not the regular `docker-compose.yml`)
3. The Portainer version doesn't need a `.env` file - it uses environment variables set in the Portainer UI

### Container Won't Start
1. Check **Logs** for error messages
2. Verify environment variables are set correctly in Portainer
3. Ensure Discord token and Google API key are valid
4. Make sure both `DISCORD_TOKEN` and `GOOGLE_API_KEY` are set in the Environment Variables section

### Bot Not Responding
1. Check container is running in **Containers** view
2. View logs for connection issues
3. Verify bot has proper Discord permissions

### Memory Issues
1. Monitor **Stats** in container view
2. Adjust memory limits in stack configuration if needed

## Security Notes

- Store API keys securely in Portainer's environment variables
- Use Portainer's access control to limit who can manage the bot
- Regularly update the container image for security patches
- Monitor logs for any suspicious activity

## Advanced Configuration

### Custom Resource Limits
In the stack editor, modify:
```yaml
deploy:
  resources:
    limits:
      memory: 1G        # Increase if needed
      cpus: '1.0'       # Increase if needed
```

### Enable Health Checks
Add to the container configuration:
```yaml
healthcheck:
  test: ["CMD", "python", "-c", "import sys; sys.exit(0)"]
  interval: 30s
  timeout: 10s
  retries: 3
```

### Auto-Updates with Watchtower
Deploy Watchtower alongside GruntBot to auto-update:
```yaml
watchtower:
  image: containrrr/watchtower
  volumes:
    - /var/run/docker.sock:/var/run/docker.sock
  command: gruntbot
```
