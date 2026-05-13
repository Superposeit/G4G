#!/bin/bash
# DeepTutor Deployment Configuration Checker
# This script checks if your configuration is ready for Dokploy deployment

echo "============================================"
echo "DeepTutor Deployment Configuration Checker"
echo "============================================"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${RED}❌ .env file not found!${NC}"
    echo "Please copy .env.example to .env and configure it."
    exit 1
fi

echo -e "${GREEN}✅ .env file found${NC}"
echo ""

# Check for required environment variables
echo "Checking required environment variables..."
echo ""

# Function to check env variable
check_env() {
    local var_name=$1
    local var_value=$(grep "^${var_name}=" .env | cut -d '=' -f2)
    local is_required=$2
    local description=$3

    if [ -z "$var_value" ] || [ "$var_value" = "your-"* ] || [ "$var_value" = "sk-your-"* ]; then
        if [ "$is_required" = "true" ]; then
            echo -e "${RED}❌ ${var_name}: ${description} (REQUIRED)${NC}"
            return 1
        else
            echo -e "${YELLOW}⚠️  ${var_name}: ${description} (OPTIONAL)${NC}"
            return 0
        fi
    else
        echo -e "${GREEN}✅ ${var_name}: ${description}${NC}"
        return 0
    fi
}

# Check critical variables
check_env "EMBEDDING_API_KEY" "true" "Embedding API key"
check_env "NEXT_PUBLIC_API_BASE_EXTERNAL" "true" "Server public URL"
check_env "LLM_BINDING" "true" "LLM provider binding"
check_env "LLM_MODEL" "true" "LLM model name"
check_env "LLM_HOST" "true" "LLM host URL"
check_env "EMBEDDING_BINDING" "true" "Embedding provider binding"
check_env "EMBEDDING_MODEL" "true" "Embedding model name"
check_env "EMBEDDING_HOST" "true" "Embedding host URL"

echo ""
echo "Checking optional environment variables..."
echo ""

check_env "BACKEND_PORT" "false" "Backend port"
check_env "FRONTEND_PORT" "false" "Frontend port"
check_env "AUTH_ENABLED" "false" "Authentication enabled"
check_env "DISABLE_SSL_VERIFY" "false" "SSL verification disabled"

echo ""
echo "Checking for Windows paths..."
echo ""

# Check for Windows paths
if grep -q "C:\\" .env; then
    echo -e "${RED}❌ Found Windows paths in .env file!${NC}"
    echo "Please remove any Windows paths (C:\\) from your .env file."
    echo "These won't work on Linux servers."
    exit 1
else
    echo -e "${GREEN}✅ No Windows paths found${NC}"
fi

echo ""
echo "Checking for placeholder values..."
echo ""

# Check for placeholder API keys
if grep -q "sk-xxx" .env || grep -q "sk-your-" .env; then
    echo -e "${RED}❌ Found placeholder API keys in .env file!${NC}"
    echo "Please replace placeholder values with actual API keys."
    exit 1
else
    echo -e "${GREEN}✅ No placeholder API keys found${NC}"
fi

echo ""
echo "Checking Docker configuration..."
echo ""

# Check if docker-compose.yml exists
if [ -f docker-compose.yml ]; then
    echo -e "${GREEN}✅ docker-compose.yml found${NC}"
else
    echo -e "${YELLOW}⚠️  docker-compose.yml not found${NC}"
fi

# Check if Dockerfile exists
if [ -f Dockerfile ]; then
    echo -e "${GREEN}✅ Dockerfile found${NC}"
else
    echo -e "${YELLOW}⚠️  Dockerfile not found${NC}"
fi

# Check if nixpacks.toml exists
if [ -f nixpacks.toml ]; then
    echo -e "${GREEN}✅ nixpacks.toml found${NC}"
else
    echo -e "${YELLOW}⚠️  nixpacks.toml not found${NC}"
fi

echo ""
echo "============================================"
echo "Configuration Check Complete!"
echo "============================================"
echo ""
echo "If all checks passed, you're ready to deploy!"
echo ""
echo "Next steps:"
echo "1. Commit your changes"
echo "2. Push to your Git repository"
echo "3. Configure Dokploy to deploy"
echo "4. Monitor the deployment logs"
echo ""
echo "For detailed deployment instructions, see DOKPLOY_DEPLOYMENT.md"
