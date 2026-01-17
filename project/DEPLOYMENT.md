# Deployment Instructions

## Orthopaedic Expert System - Production Deployment Guide

This guide provides step-by-step instructions for deploying the system to production environments.

## Prerequisites

- Server with Ubuntu 20.04+ or similar Linux distribution
- Python 3.8 or higher
- PostgreSQL access (Supabase account)
- Domain name (optional but recommended)
- SSL certificate (Let's Encrypt recommended)
- 4GB RAM minimum, 8GB recommended
- 20GB disk space minimum

## Deployment Options

### Option 1: Cloud Deployment (Recommended)

#### Backend Deployment (FastAPI on Render/Railway/Heroku)

1. **Prepare the repository**:
```bash
git init
git add .
git commit -m "Initial commit"
```

2. **Create Procfile** (for Heroku/Railway):
```
web: cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
```

3. **Deploy to Render**:
   - Go to https://render.com
   - Create new "Web Service"
   - Connect your GitHub repository
   - Set build command: `cd backend && pip install -r requirements.txt && python -m spacy download en_core_web_sm`
   - Set start command: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Add environment variables from `.env`
   - Deploy

4. **Deploy to Railway**:
   - Go to https://railway.app
   - Create new project from GitHub repo
   - Add environment variables
   - Railway will auto-detect Python and deploy

#### Frontend Deployment (Streamlit Cloud)

1. **Deploy to Streamlit Cloud**:
   - Go to https://streamlit.io/cloud
   - Connect GitHub repository
   - Select `streamlit_app/app.py` as main file
   - Add secrets (environment variables):
     ```toml
     API_BASE_URL = "https://your-api-url.com"
     ```
   - Deploy

### Option 2: Self-Hosted Deployment

#### Backend Setup

1. **Server Setup**:
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv nginx supervisor -y
```

2. **Clone and setup**:
```bash
cd /opt
git clone <your-repo-url> ortho-expert
cd ortho-expert/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

3. **Configure environment**:
```bash
cp .env.example .env
nano .env
```

Add your production credentials.

4. **Create systemd service** `/etc/systemd/system/ortho-api.service`:
```ini
[Unit]
Description=Orthopaedic Expert System API
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/ortho-expert/backend
Environment="PATH=/opt/ortho-expert/backend/venv/bin"
ExecStart=/opt/ortho-expert/backend/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

[Install]
WantedBy=multi-user.target
```

5. **Start service**:
```bash
sudo systemctl daemon-reload
sudo systemctl enable ortho-api
sudo systemctl start ortho-api
sudo systemctl status ortho-api
```

6. **Configure Nginx** `/etc/nginx/sites-available/ortho-api`:
```nginx
server {
    listen 80;
    server_name api.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

7. **Enable site and SSL**:
```bash
sudo ln -s /etc/nginx/sites-available/ortho-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d api.yourdomain.com
```

#### Frontend Setup

1. **Install Streamlit**:
```bash
cd /opt/ortho-expert/streamlit_app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. **Configure environment**:
```bash
cp .env.example .env
nano .env
```

Set `API_BASE_URL` to your backend URL.

3. **Create systemd service** `/etc/systemd/system/ortho-streamlit.service`:
```ini
[Unit]
Description=Orthopaedic Expert System Frontend
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/ortho-expert/streamlit_app
Environment="PATH=/opt/ortho-expert/streamlit_app/venv/bin"
ExecStart=/opt/ortho-expert/streamlit_app/venv/bin/streamlit run app.py --server.port 8501 --server.address 0.0.0.0

[Install]
WantedBy=multi-user.target
```

4. **Start service**:
```bash
sudo systemctl daemon-reload
sudo systemctl enable ortho-streamlit
sudo systemlit start ortho-streamlit
```

5. **Configure Nginx** `/etc/nginx/sites-available/ortho-frontend`:
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8501;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

6. **Enable and secure**:
```bash
sudo ln -s /etc/nginx/sites-available/ortho-frontend /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
sudo certbot --nginx -d yourdomain.com
```

### Option 3: Docker Deployment

1. **Create `backend/Dockerfile`**:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m spacy download en_core_web_sm

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

2. **Create `streamlit_app/Dockerfile`**:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["streamlit", "run", "app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
```

3. **Create `docker-compose.yml`** in project root:
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - SUPABASE_URL=${SUPABASE_URL}
      - SUPABASE_ANON_KEY=${SUPABASE_ANON_KEY}
      - SUPABASE_SERVICE_KEY=${SUPABASE_SERVICE_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    restart: always

  frontend:
    build: ./streamlit_app
    ports:
      - "8501:8501"
    environment:
      - API_BASE_URL=http://backend:8000
    depends_on:
      - backend
    restart: always
```

4. **Deploy**:
```bash
docker-compose up -d
```

## Database Migration

The database schema is automatically created via the Supabase migration system when the backend first connects.

To manually verify:

1. Log into Supabase Dashboard
2. Go to SQL Editor
3. Check that all tables exist:
   - patients
   - symptoms
   - predictions
   - recommendations
   - appointments
   - consultation_logs
   - model_performance

## Post-Deployment Configuration

### 1. Test API Health

```bash
curl https://api.yourdomain.com/health
```

Expected response:
```json
{"status": "healthy", "service": "orthopaedic-expert-system"}
```

### 2. Test Frontend Access

Open browser: `https://yourdomain.com`

### 3. Create Test Patient

Use the Patient Intake form to register a test patient and verify the full workflow.

### 4. Monitor Logs

**Backend logs**:
```bash
sudo journalctl -u ortho-api -f
```

**Frontend logs**:
```bash
sudo journalctl -u ortho-streamlit -f
```

### 5. Setup Monitoring (Optional)

Use tools like:
- **Sentry** for error tracking
- **Datadog** for performance monitoring
- **Uptime Robot** for availability monitoring

## Security Checklist

- [ ] Environment variables are secure (not committed to git)
- [ ] SSL/TLS certificates are active
- [ ] Firewall configured (only ports 80, 443, 22 open)
- [ ] Database uses strong passwords
- [ ] Row-Level Security enabled on all Supabase tables
- [ ] API rate limiting configured
- [ ] Regular security updates scheduled
- [ ] Backup strategy implemented
- [ ] User authentication enabled
- [ ] HIPAA compliance measures in place

## Backup Strategy

### Database Backups (Supabase)

Supabase automatically backs up your database. To export manually:

1. Go to Supabase Dashboard
2. Settings → Database → Connection Info
3. Use `pg_dump` to create backups:

```bash
pg_dump -h db.xxx.supabase.co -U postgres -d postgres > backup.sql
```

### Application Backups

```bash
tar -czf ortho-expert-backup-$(date +%Y%m%d).tar.gz /opt/ortho-expert
```

Schedule daily backups:
```bash
0 2 * * * /usr/local/bin/backup-ortho-expert.sh
```

## Scaling Considerations

### Horizontal Scaling

1. **Load Balancer**: Use Nginx or HAProxy
2. **Multiple API Instances**: Run multiple uvicorn workers
3. **Database Connection Pooling**: Configure pgBouncer

### Performance Optimization

1. **Redis Caching**: Cache frequent predictions
2. **CDN**: Serve static assets via CDN
3. **Database Indexing**: Already configured in migration
4. **Async Processing**: Use Celery for heavy ML tasks

## Troubleshooting

### Backend won't start

```bash
sudo journalctl -u ortho-api -n 100
```

Check:
- Environment variables are set
- Python virtual environment is activated
- All dependencies installed
- Port 8000 not in use

### Frontend connection issues

Check:
- `API_BASE_URL` in `.env` is correct
- Backend is running and accessible
- No CORS issues (check backend logs)

### Database connection errors

Verify:
- Supabase credentials are correct
- Project is not paused (free tier)
- IP address is allowed (if IP restrictions enabled)

## Maintenance

### Update Application

```bash
cd /opt/ortho-expert
git pull
cd backend
source venv/bin/activate
pip install -r requirements.txt --upgrade
sudo systemctl restart ortho-api

cd ../streamlit_app
source venv/bin/activate
pip install -r requirements.txt --upgrade
sudo systemctl restart ortho-streamlit
```

### Monitor Performance

```bash
htop
df -h
sudo tail -f /var/log/nginx/access.log
```

## Support

For deployment issues:
- Check logs first
- Review Supabase dashboard for database issues
- Verify all environment variables
- Test API endpoints individually

## Production Checklist

Before going live:

- [ ] All tests pass
- [ ] Environment variables configured
- [ ] SSL certificates active
- [ ] Monitoring enabled
- [ ] Backups configured
- [ ] Documentation complete
- [ ] Security audit performed
- [ ] Load testing completed
- [ ] Disaster recovery plan in place
- [ ] Team trained on system usage

## Compliance Notes

For healthcare deployment:

- Ensure HIPAA compliance if handling PHI
- Implement audit logging
- Encrypt data at rest and in transit
- Regular security assessments
- Business Associate Agreements (BAA) with vendors
- Incident response plan
- Data retention policies

---

**Version**: 1.0.0
**Last Updated**: December 2024
