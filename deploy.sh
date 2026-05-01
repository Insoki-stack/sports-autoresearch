#!/bin/bash
# deploy.sh - Deploy dashboard to cloud (Render.com)
# This script deploys the Flask app to Render for free hosting

echo "Deploying Sports Autoresearch Dashboard to Render..."

# Check if render CLI is installed
if ! command -v render &> /dev/null
then
    echo "Installing Render CLI..."
    npm install -g @render/cli
fi

# Deploy to Render
render deploy

echo "Dashboard deployed! You can access it at your Render URL."
echo "Make sure to set environment variables:"
echo "- ODDS_API_KEY=da6e9aec8a38554193953371d6a8dca5"
