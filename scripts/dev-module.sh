#!/bin/bash
# Master Controller for Care4Animals Module Development

MODULE=$1 # e.g., analytics, sms, cms
ACTION=$2 # e.g., sync, db-check, test, seed, deps

# Colors for better readability
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

case $ACTION in
  "sync")
    echo -e "${BLUE}🔄 Syncing Backend for $MODULE...${NC}"
    docker compose restart backend
    echo -e "${GREEN}✅ Backend restarted.${NC}"
    ;;
  
  "deps")
    echo -e "${BLUE}📦 Installing Python dependencies...${NC}"
    docker compose exec backend pip install python-docx requests
    echo -e "${GREEN}✅ Dependencies installed.${NC}"
    ;;

  "db-check")
    echo -e "${BLUE}🗄️ Verifying Database Tables...${NC}"
    docker compose exec db psql -U care4animals -d care4animals -c "\dt"
    ;;

 "seed")
    echo -e "${BLUE}🌱 Starting Multilingual Seed (EN, LG, SW)...${NC}"
    for lang in en lg sw; do
      echo -e "${BLUE}➔ Processing ${lang}.docx...${NC}"
      # We use 'scripts/...' because '/app/backend/scripts/...' doesn't exist inside the container
      docker compose exec backend python scripts/seed_lessons_via_api.py --file seed/${lang}.docx
    done
    echo -e "${GREEN}✅ Seeding process complete.${NC}"
    ;;

  "test")
    echo -e "${BLUE}🧪 Running Integration Test for $MODULE...${NC}"
    if [ -f "scripts/tests/test_${MODULE}.sh" ]; then
        bash scripts/tests/test_${MODULE}.sh
    else
        echo -e "${RED}❌ Test script scripts/tests/test_${MODULE}.sh not found!${NC}"
    fi
    ;;

  *)
    echo "Usage: ./scripts/dev-module.sh [module_name] [sync|db-check|seed|test|deps]"
    ;;
esac