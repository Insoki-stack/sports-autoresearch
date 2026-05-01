# Keep Bot Running in Background

## Option 1: Cloud Deployment (Recommended - Easiest)

### Deploy to Render.com (Free)
This is the easiest way - your bot runs 24/7 in the cloud:

1. **Push to GitHub**
```bash
git add .
git commit -m "Ready for deployment"
git push origin autoresearch/may1
```

2. **Deploy to Render**
- Go to render.com (free account)
- Click "New +" → "Web Service"
- Connect your GitHub repository
- Use `render.yaml` configuration (already in project)
- Click "Deploy"

3. **Access from Anywhere**
- Your dashboard will be at: `https://your-app.onrender.com`
- Works on phone, tablet, laptop - anywhere
- Bot runs 24/7, no need to keep laptop open

### Benefits:
- ✅ Runs 24/7 automatically
- ✅ Access from anywhere
- ✅ Free tier available
- ✅ Auto-updates when you push code
- ✅ SSL/HTTPS included

## Option 2: Run as Windows Service

### Install NSSM (Non-Sucking Service Manager)
1. Download from: https://nssm.cc/download
2. Extract and run `nssm.exe` as administrator

### Create Service
```bash
nssm install SportsBot
```
- Path: `C:\Users\Boydb\.local\bin\uv.exe`
- Startup directory: `C:\Users\Boydb\CascadeProjects\windsurf-project\sports-autoresearch`
- Arguments: `run python app.py`

### Start Service
```bash
nssm start SportsBot
```

### Benefits:
- ✅ Runs when Windows starts
- ✅ Runs in background
- ✅ Survives laptop sleep/close
- ❌ Only accessible on your local network

## Option 3: Screen/Session (For Advanced Users)

### Using tmux (Linux/Mac) or Windows Terminal
```bash
# Install tmux if not available
# Windows: Use WSL or Git Bash

# Create session
tmux new -s sportsbot

# Start bot
cd sports-autoresearch
uv run python app.py

# Detach (Ctrl+B, then D)
# Bot continues running in background

# Reattach later
tmux attach -t sportsbot
```

### Benefits:
- ✅ Free
- ❌ Requires technical knowledge
- ❌ Doesn't survive computer restart

## Option 4: VPS/Cloud Server

### Rent a VPS (DigitalOcean, Linode, AWS Lightsail)
- Cost: ~$5/month
- Set up Ubuntu server
- Deploy bot using Docker or direct Python
- Access via domain name

### Benefits:
- ✅ Full control
- ✅ Reliable
- ❌ Costs money
- ❌ Requires server setup knowledge

## Recommended: Render.com

**Why Render.com is best for you:**
1. **Free tier available** - no cost
2. **Easiest setup** - just connect GitHub
3. **24/7 uptime** - runs automatically
4. **Mobile access** - check bets from phone anywhere
5. **Auto-updates** - push code and it deploys
6. **SSL included** - secure connection

## Quick Start for Render Deployment:

1. Push code to GitHub
2. Go to render.com
3. Connect GitHub repo
4. Deploy using `render.yaml`
5. Done! Your bot is live.

Your dashboard will be accessible at a URL like: `https://sports-autoresearch.onrender.com`

You can check it from your phone while out and about, and the bot keeps running 24/7 without needing your laptop to be open.
