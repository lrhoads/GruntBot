#!/bin/bash

# GruntBot Portainer Deployment Script
# This script helps prepare GruntBot for Portainer deployment

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# ASCII Art
show_banner() {
    echo -e "${GREEN}"
    cat << "EOF"
  ____                  _   ____        _   
 / ___|_ __ _   _ _ __ | |_| __ )  ___ | |_ 
| |  _| '__| | | | '_ \| __|  _ \ / _ \| __|
| |_| | |  | |_| | | | | |_| |_) | (_) | |_ 
 \____|_|   \__,_|_| |_|\__|____/ \___/ \__|
                                           
        Portainer Deployment Helper
EOF
    echo -e "${NC}"
}

# Check prerequisites
check_prerequisites() {
    log_step "Checking prerequisites..."
    
    # Check if git is available
    if ! command -v git &> /dev/null; then
        log_error "Git is not installed or not in PATH"
        exit 1
    fi
    
    # Check if we're in a git repository
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        log_error "Not in a Git repository"
        exit 1
    fi
    
    log_info "Prerequisites check passed"
}

# Create necessary directories
create_directories() {
    log_step "Creating necessary directories..."
    
    mkdir -p logs
    mkdir -p res
    
    log_info "Directories created"
}

# Generate environment template
generate_env_template() {
    log_step "Generating environment template..."
    
    if [ ! -f .env.portainer ]; then
        cat > .env.portainer << EOF
# GruntBot Environment Variables for Portainer
# Copy these values to your Portainer stack environment variables

DISCORD_TOKEN=your_discord_bot_token_here
GOOGLE_API_KEY=your_google_generative_ai_api_key_here

# Optional: Uncomment and modify if needed
# PYTHONPATH=/app
# PYTHONUNBUFFERED=1
EOF
        log_info "Created .env.portainer template"
    else
        log_info ".env.portainer already exists"
    fi
}

# Build image locally (optional)
build_image() {
    log_step "Building Docker image locally..."
    
    if command -v docker &> /dev/null; then
        docker build -t gruntbot:latest .
        log_info "Docker image built successfully"
    else
        log_warn "Docker not found, skipping local build"
        log_info "Image will be built when deployed in Portainer"
    fi
}

# Generate Portainer stack YAML
generate_stack_yaml() {
    log_step "Generating Portainer stack configuration..."
    
    cat > portainer-stack.yml << 'EOF'
version: '3.8'

services:
  gruntbot:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: gruntbot
    restart: unless-stopped
    environment:
      - DISCORD_TOKEN=${DISCORD_TOKEN}
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
      - PYTHONPATH=/app
      - PYTHONUNBUFFERED=1
    volumes:
      - gruntbot-profiles:/app/res
      - gruntbot-logs:/app/logs
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '0.5'
        reservations:
          memory: 256M
          cpus: '0.25'
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
    labels:
      - "io.portainer.accesscontrol.teams=administrators"
      - "description=GruntBot Discord Bot with AI Learning"
      - "maintainer=GruntBot Team"
      - "version=latest"

volumes:
  gruntbot-profiles:
    driver: local
  gruntbot-logs:
    driver: local

networks:
  default:
    name: gruntbot-network
    labels:
      - "description=GruntBot Network"
EOF
    
    log_info "Generated portainer-stack.yml"
}

# Show deployment instructions
show_instructions() {
    log_step "Deployment Instructions"
    
    echo ""
    echo -e "${YELLOW}=== PORTAINER DEPLOYMENT STEPS ===${NC}"
    echo ""
    echo "1. Push your code to GitHub:"
    echo "   git add ."
    echo "   git commit -m 'Add Portainer configuration'"
    echo "   git push origin main"
    echo ""
    echo "2. In Portainer:"
    echo "   - Go to 'Stacks' → 'Add stack'"
    echo "   - Name: gruntbot"
    echo "   - Build method: Git Repository"
    echo "   - Repository URL: $(git config --get remote.origin.url)"
    echo "   - Reference: refs/heads/main"
    echo "   - Compose path: docker-compose.portainer.yml"
    echo ""
    echo "3. Add Environment Variables:"
    echo "   - DISCORD_TOKEN: [Your Discord bot token]"
    echo "   - GOOGLE_API_KEY: [Your Google AI API key]"
    echo ""
    echo "4. Deploy the stack!"
    echo ""
    echo -e "${GREEN}Environment template created in .env.portainer${NC}"
    echo -e "${GREEN}Full guide available in PORTAINER.md${NC}"
    echo ""
}

# Validate configuration
validate_config() {
    log_step "Validating configuration..."
    
    # Check if required files exist
    required_files=("Dockerfile" "docker-compose.portainer.yml" "src/main.py" "requirements.txt")
    
    for file in "${required_files[@]}"; do
        if [ ! -f "$file" ]; then
            log_error "Required file missing: $file"
            exit 1
        fi
    done
    
    log_info "Configuration validation passed"
}

# Main execution
main() {
    show_banner
    
    check_prerequisites
    create_directories
    generate_env_template
    validate_config
    
    # Ask if user wants to build locally
    echo ""
    read -p "Build Docker image locally for testing? (y/N): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        build_image
    fi
    
    generate_stack_yaml
    show_instructions
    
    log_info "Portainer deployment preparation complete!"
}

# Handle script arguments
case "${1:-help}" in
    prepare)
        main
        ;;
    validate)
        validate_config
        ;;
    env)
        generate_env_template
        ;;
    help|*)
        echo "GruntBot Portainer Helper Script"
        echo ""
        echo "Usage: $0 {prepare|validate|env|help}"
        echo ""
        echo "Commands:"
        echo "  prepare  - Full preparation for Portainer deployment"
        echo "  validate - Validate configuration files"
        echo "  env      - Generate environment template"
        echo "  help     - Show this help message"
        ;;
esac
