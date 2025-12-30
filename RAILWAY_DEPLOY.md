# Railway Deployment Guide for n8n

## Quick Setup

### 1. Environment Variables (Required in Railway)

Add these in Railway's service settings:

```bash
# Authentication (Required)
N8N_BASIC_AUTH_USER=your-admin-username
N8N_BASIC_AUTH_PASSWORD=your-secure-password

# Security Keys (Required - generate random 32+ char strings)
N8N_ENCRYPTION_KEY=your-32-char-random-encryption-key
N8N_JWT_SECRET=your-32-char-random-jwt-secret

# Webhook URL (use Railway's provided domain)
WEBHOOK_URL=https://${{RAILWAY_PUBLIC_DOMAIN}}
N8N_EDITOR_BASE_URL=https://${{RAILWAY_PUBLIC_DOMAIN}}
```

### 2. Add PostgreSQL Database

1. In Railway dashboard, click "+ New"
2. Select "Database" → "PostgreSQL"
3. Railway automatically sets these variables:
   - `PGHOST`
   - `PGPORT`
   - `PGDATABASE`
   - `PGUSER`
   - `PGPASSWORD`

4. Link them to your n8n service:
```bash
DB_TYPE=postgresdb
DB_POSTGRESDB_HOST=${{PGHOST}}
DB_POSTGRESDB_PORT=${{PGPORT}}
DB_POSTGRESDB_DATABASE=${{PGDATABASE}}
DB_POSTGRESDB_USER=${{PGUSER}}
DB_POSTGRESDB_PASSWORD=${{PGPASSWORD}}
```

### 3. Optional: Add Redis (Recommended for Production)

1. In Railway dashboard, click "+ New"
2. Select "Database" → "Redis"
3. Railway automatically sets:
   - `REDIS_HOST`
   - `REDIS_PORT`
   - `REDIS_PASSWORD`

4. Link them:
```bash
QUEUE_BULL_REDIS_HOST=${{REDIS_HOST}}
QUEUE_BULL_REDIS_PORT=${{REDIS_PORT}}
QUEUE_BULL_REDIS_PASSWORD=${{REDIS_PASSWORD}}
```

### 4. Generate Secure Keys

Use these commands to generate secure random keys:

**Windows PowerShell:**
```powershell
# Generate encryption key
-join ((33..126) | Get-Random -Count 32 | % {[char]$_})

# Generate JWT secret
-join ((33..126) | Get-Random -Count 32 | % {[char]$_})
```

**Linux/Mac:**
```bash
# Generate encryption key
openssl rand -base64 32

# Generate JWT secret
openssl rand -base64 32
```

### 5. Complete Environment Variables List

Copy this template to Railway:

```bash
# Basic Auth
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=your-secure-password

# Security
N8N_ENCRYPTION_KEY=your-32-char-encryption-key
N8N_JWT_SECRET=your-32-char-jwt-secret
N8N_SECURE_COOKIE=true

# URLs
WEBHOOK_URL=https://${{RAILWAY_PUBLIC_DOMAIN}}
N8N_EDITOR_BASE_URL=https://${{RAILWAY_PUBLIC_DOMAIN}}
N8N_PROTOCOL=https
N8N_PORT=5678

# Database (PostgreSQL)
DB_TYPE=postgresdb
DB_POSTGRESDB_HOST=${{PGHOST}}
DB_POSTGRESDB_PORT=${{PGPORT}}
DB_POSTGRESDB_DATABASE=${{PGDATABASE}}
DB_POSTGRESDB_USER=${{PGUSER}}
DB_POSTGRESDB_PASSWORD=${{PGPASSWORD}}

# Redis (Optional but recommended)
QUEUE_BULL_REDIS_HOST=${{REDIS_HOST}}
QUEUE_BULL_REDIS_PORT=${{REDIS_PORT}}
QUEUE_BULL_REDIS_PASSWORD=${{REDIS_PASSWORD}}

# Execution
EXECUTIONS_MODE=regular
EXECUTIONS_TIMEOUT=3600
EXECUTIONS_TIMEOUT_MAX=7200

# Timezone
GENERIC_TIMEZONE=UTC

# Logging
N8N_LOG_LEVEL=info
N8N_LOG_OUTPUT=console
```

## Deployment Checklist

- [ ] Fork/Clone repository to your GitHub
- [ ] Create new Railway project
- [ ] Connect GitHub repository
- [ ] Add PostgreSQL database service
- [ ] (Optional) Add Redis service
- [ ] Set all required environment variables
- [ ] Deploy!
- [ ] Access n8n at your Railway domain

## Post-Deployment

### Access n8n
Your n8n instance will be available at:
```
https://your-service-name.railway.app
```

### Login
Use the credentials you set:
- **Username:** Value from `N8N_BASIC_AUTH_USER`
- **Password:** Value from `N8N_BASIC_AUTH_PASSWORD`

### Health Check
```bash
curl https://your-service-name.railway.app/healthz
```

### View Logs
In Railway dashboard → Your Service → "Deployments" → Click on deployment → "View Logs"

## Troubleshooting

### Database Connection Issues
- Ensure PostgreSQL service is linked to n8n service
- Verify all `DB_POSTGRESDB_*` variables are set correctly
- Check PostgreSQL service is running

### Authentication Issues
- Verify `N8N_BASIC_AUTH_USER` and `N8N_BASIC_AUTH_PASSWORD` are set
- Try clearing browser cookies/cache
- Check `N8N_BASIC_AUTH_ACTIVE=true` is set

### Webhook Issues
- Ensure `WEBHOOK_URL` uses `${{RAILWAY_PUBLIC_DOMAIN}}`
- Check Railway has assigned a public domain
- Verify `N8N_PROTOCOL=https`

### Build Failures
- Check Railway build logs for errors
- Ensure Dockerfile exists and is valid
- Verify repository has all required files

## Scaling

Railway automatically handles:
- ✅ HTTPS/SSL certificates
- ✅ Load balancing
- ✅ Auto-restarts on failures
- ✅ Environment variable management
- ✅ Database backups (PostgreSQL)

## Support

- **n8n Documentation:** https://docs.n8n.io
- **Railway Documentation:** https://docs.railway.app
- **GitHub Issues:** https://github.com/krishnashakula/LinkedinBOT/issues
