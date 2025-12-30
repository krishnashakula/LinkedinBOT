# Setting Up Railway GitHub Actions Auto-Deployment

## Option 1: Manual Deployment (Recommended for Getting Started)

Railway automatically deploys when you push to GitHub. No GitHub Actions needed!

1. Go to Railway dashboard
2. Connect your GitHub repository
3. Railway will auto-deploy on every push to main branch

**This is the easiest method and already works!**

---

## Option 2: GitHub Actions Deployment (Optional)

If you want to use GitHub Actions for deployment:

### Step 1: Get Railway Token

1. Go to https://railway.app/account/tokens
2. Click "Create New Token"
3. Give it a name (e.g., "GitHub Actions")
4. Copy the token (you won't see it again!)

### Step 2: Add Token to GitHub

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `RAILWAY_TOKEN`
5. Value: Paste your Railway token
6. Click **Add secret**

### Step 3: Push to Trigger Deployment

```bash
git push origin main
```

The GitHub Action will now automatically deploy to Railway!

---

## Disable GitHub Actions Deployment

If you only want Railway's built-in auto-deploy (recommended):

1. Delete or rename `.github/workflows/deploy.yml`
2. Railway will still auto-deploy on every push

Or simply don't set the `RAILWAY_TOKEN` secret - the workflow will skip gracefully.

---

## Troubleshooting

### "RAILWAY_TOKEN not found" Error

- The workflow skips automatically if token is not set
- Railway's native auto-deploy still works!
- No action needed unless you specifically want GitHub Actions deployment

### Token Invalid

- Regenerate token at https://railway.app/account/tokens
- Update GitHub secret with new token

### Deployment Not Triggering

- Check Railway dashboard for build logs
- Ensure repository is connected to Railway
- Verify you're pushing to the `main` branch
