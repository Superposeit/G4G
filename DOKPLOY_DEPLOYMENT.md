# DeepTutor Dokploy Deployment Guide

## 🚀 Quick Start

### Prerequisites
- Dokploy server running on Ubuntu 24.04
- Git repository with your DeepTutor code
- At least 4GB RAM and 5GB disk space available

### Step 1: Get Your Embedding API Key

**Option A: SiliconFlow (Free)**
1. Go to https://cloud.siliconflow.cn/account/ak
2. Sign up and create an API key
3. Copy your API key

**Option B: Jina AI (Free)**
1. Go to https://jina.ai/
2. Sign up and get your API key
3. Copy your API key

**Option C: OpenAI (Paid)**
1. Go to https://platform.openai.com/api-keys
2. Create an API key
3. Copy your API key

### Step 2: Update Your .env File

Edit `.env` in your repository and update these values:

```env
# Replace with your actual API key
EMBEDDING_API_KEY=sk-your-actual-api-key-here

# Set your server's public URL
NEXT_PUBLIC_API_BASE_EXTERNAL=https://your-domain.com
# OR use IP: http://your-server-ip:8001
```

### Step 3: Configure Dokploy

#### Option A: Using Docker Compose (Recommended)

1. In Dokploy, create a new project
2. Select "Docker Compose" as the deployment type
3. Connect your Git repository
4. Set the build context to the repository root
5. Use `docker-compose.yml` as the compose file

**Important:** Make sure Dokploy deploys ALL services:
- `litertlm` (LLM backend)
- `pocketbase` (auth/storage)
- `deeptutor` (main application)

#### Option B: Using Nixpacks

1. In Dokploy, create a new project
2. Select "Nixpacks" as the deployment type
3. Connect your Git repository
4. The `nixpacks.toml` file will be used automatically

**Note:** Nixpacks only deploys the backend. You'll need to deploy the frontend separately or use Docker Compose.

### Step 4: Configure Environment Variables in Dokploy

In Dokploy, add these environment variables:

```env
# Ports
BACKEND_PORT=8001
FRONTEND_PORT=3782

# LLM Configuration
LLM_BINDING=litertlm
LLM_MODEL=gemma-4-E2B-it
LLM_API_KEY=sk-no-key-required
LLM_HOST=http://litertlm:8000/v1

# LiteRT-LM Bridge
LITERTLM_HOST=0.0.0.0
LITERTLM_PORT=8000
LITERTLM_MODEL_ID=gemma-4-E2B-it
LITERTLM_LOG_LEVEL=INFO

# Embedding Configuration (use your actual API key)
EMBEDDING_BINDING=siliconflow
EMBEDDING_MODEL=BAAI/bge-large-en-v1.5
EMBEDDING_API_KEY=your-actual-api-key-here
EMBEDDING_HOST=https://api.siliconflow.cn/v1/embeddings
EMBEDDING_DIMENSION=1024

# Server URL (IMPORTANT for remote deployment)
NEXT_PUBLIC_API_BASE_EXTERNAL=https://your-domain.com

# Security
DISABLE_SSL_VERIFY=false
AUTH_ENABLED=false
```

### Step 5: Configure Port Mapping

Make sure these ports are exposed:
- **8001** - Backend API
- **3782** - Frontend web interface
- **8000** - LiteRT-LM bridge (internal)
- **8090** - PocketBase (internal)

### Step 6: Deploy

1. Push your changes to Git
2. Trigger deployment in Dokploy
3. Wait for the build to complete
4. Check the logs for any errors

## 🔍 Troubleshooting

### Container starts and immediately stops

**Check the logs:**
```bash
docker logs <container-name>
```

**Common issues:**
1. Missing API key - Update `EMBEDDING_API_KEY`
2. Invalid server URL - Update `NEXT_PUBLIC_API_BASE_EXTERNAL`
3. Port conflicts - Check if ports are already in use
4. Insufficient resources - Ensure at least 4GB RAM available

### Frontend can't connect to backend

**Check:**
1. `NEXT_PUBLIC_API_BASE_EXTERNAL` is set correctly
2. Backend service is running and healthy
3. Firewall allows traffic on port 8001

### Model download takes too long

The first deployment will download the 2.5GB Gemma model. This can take 5-10 minutes depending on your internet connection.

### Services can't communicate

Make sure all services are on the same Docker network (`deeptutor-network`).

## 📊 Monitoring

### Check service status:
```bash
docker ps
```

### View logs:
```bash
docker logs -f deeptutor
docker logs -f litertlm
docker logs -f pocketbase
```

### Check health:
```bash
curl http://localhost:8001/
curl http://localhost:8000/health
```

## 🔒 Security

For production deployments:

1. **Enable authentication:**
   ```env
   AUTH_ENABLED=true
   AUTH_SECRET=<generate-with-python>
   ```

2. **Use HTTPS:**
   ```env
   AUTH_COOKIE_SECURE=true
   NEXT_PUBLIC_API_BASE_EXTERNAL=https://your-domain.com
   ```

3. **Generate secure secret:**
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

## 📝 Additional Notes

- The LiteRT-LM service will automatically download the model on first startup
- Model files are persisted in `./data/models/` directory
- User data is stored in `./data/user/` directory
- Knowledge bases are stored in `./data/knowledge_bases/` directory

## 🆘 Support

If you encounter issues:
1. Check container logs first
2. Verify all environment variables are set correctly
3. Ensure all services are running
4. Check network connectivity between services

## 🎯 Success Indicators

Your deployment is successful when:
- ✅ All 3 services are running (deeptutor, litertlm, pocketbase)
- ✅ Backend responds to `http://your-server:8001/`
- ✅ Frontend loads at `http://your-server:3782`
- ✅ LiteRT-LM health check passes
- ✅ No errors in container logs
