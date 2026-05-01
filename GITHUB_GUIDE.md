# GitHub Guide for Beginners - Step by Step

## What is GitHub?
GitHub is a website where you store your code online. It's like Google Drive but for code. We'll use it to deploy your sports bot to Render.com so it runs 24/7.

## Step 1: Create a GitHub Account

1. Go to https://github.com
2. Click "Sign up" (top right)
3. Enter:
   - Username: Pick something easy to remember (e.g., yourname-sportsbot)
   - Email: Your email
   - Password: Create a strong password
4. Click "Create account"
5. Check your email and verify your account
6. Skip the "Create a repository" page for now

## Step 2: Install Git on Your Computer

Git is the tool that talks to GitHub from your computer.

**For Windows:**
1. Go to https://git-scm.com/download/win
2. Download the installer
3. Run the installer
4. Click "Next" through all the default options
5. Click "Finish" when done

**Verify Git is installed:**
1. Open PowerShell (search "PowerShell" in Windows)
2. Type: `git --version`
3. If you see a version number (like git version 2.x.x), it's installed!

## Step 3: Connect Your Computer to GitHub

1. Open PowerShell
2. Type: `git config --global user.name "YOUR_USERNAME"`
   - Replace YOUR_USERNAME with your GitHub username
3. Type: `git config --global user.email "YOUR_EMAIL"`
   - Replace YOUR_EMAIL with your GitHub email

## Step 4: Create a GitHub Repository

1. Go to https://github.com and log in
2. Click the "+" icon (top right) → "New repository"
3. Fill in:
   - Repository name: `sports-autoresearch` (or whatever you want)
   - Description: `AI Sports Betting Bot`
   - Make it **Public** (required for Render.com free tier)
   - **DO NOT** check "Add a README file" (we already have one)
4. Click "Create repository"

**You'll see a page with instructions. Keep this open!**

## Step 5: Push Your Code to GitHub

1. Go to your project folder in PowerShell:
```powershell
cd C:\Users\Boydb\CascadeProjects\windsurf-project\sports-autoresearch
```

2. Initialize git (if not already done):
```powershell
git init
```

3. Add all your files:
```powershell
git add .
```

4. Commit your files:
```powershell
git commit -m "Initial commit"
```

5. Connect to your GitHub repository:
```powershell
git remote add origin https://github.com/YOUR_USERNAME/sports-autoresearch.git
```
- Replace YOUR_USERNAME with your GitHub username

6. Push your code:
```powershell
git branch -M main
git push -u origin main
```

7. **It will ask for your GitHub username and password**
   - Username: Your GitHub username
   - Password: **NOT your regular password!**
   - You need a Personal Access Token (see below)

## Step 6: Create a Personal Access Token (Required for GitHub)

GitHub no longer accepts passwords. You need a token instead.

1. Go to https://github.com and log in
2. Click your profile picture (top right) → "Settings"
3. On the left, click "Developer settings"
4. Click "Personal access tokens" → "Tokens (classic)"
5. Click "Generate new token" → "Generate new token (classic)"
6. Fill in:
   - Note: "Sports Bot Deployment"
   - Expiration: "No expiration" or choose a date
   - **Check these boxes:**
     - ✅ repo (full control)
     - ✅ workflow
7. Click "Generate token"
8. **COPY THE TOKEN IMMEDIATELY** (you won't see it again!)
   - It looks like: `ghp_xxxxxxxxxxxxxxxxxxxx`

9. Go back to PowerShell and try the push again:
```powershell
git push -u origin main
```
10. When asked for password, paste your token (not your password)

## Step 7: Verify Your Code is on GitHub

1. Go to https://github.com/YOUR_USERNAME/sports-autoresearch (e.g., https://github.com/Insoki-stack/sports-autoresearch)
2. You should see all your files there!
3. Success! Your code is now on GitHub.

## Step 8: Deploy to Render.com

Now that your code is on GitHub, deploying is easy:

1. Go to https://render.com
2. Click "Sign up" (top right)
3. Sign up with GitHub (click "Sign up with GitHub")
4. Authorize Render to access your GitHub
5. Click "New +" (top right) → "Web Service"
6. Click "Connect" next to your sports-autoresearch repository
7. Fill in:
   - Name: `sports-autoresearch` (or whatever)
   - Region: Oregon (or closest to you)
   - Branch: `main`
   - Runtime: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
8. Click "Create Web Service"
9. Wait a few minutes for it to deploy
10. Your dashboard will be at: `https://sports-autoresearch.onrender.com`

## Troubleshooting

**"fatal: repository already exists"**
```powershell
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/sports-autoresearch.git
```

**"Authentication failed"**
- Make sure you're using your Personal Access Token, not your password
- Generate a new token if needed

**"Permission denied"**
- Make sure your GitHub repository is Public
- Check that Render has access to your GitHub

## Next Steps

Once deployed:
1. Your bot runs 24/7 automatically
2. Access your dashboard from anywhere
3. Close your laptop - bot keeps running!
4. Check predictions from your phone

## Quick Reference Commands

```powershell
# After making changes to your code:
git add .
git commit -m "Description of changes"
git push

# Check status:
git status

# See recent commits:
git log --oneline
```

That's it! Your code is now on GitHub and deployed to Render.com.
