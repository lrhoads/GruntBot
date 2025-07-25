#!/bin/bash

# GruntBot Docker Management Script

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
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

# Check if .env file exists
check_env() {
    if [ ! -f .env ]; then
        log_error ".env file not found!"
        log_info "Please create a .env file with your Discord and Google API keys:"
        echo "DISCORD_TOKEN=your_discord_token_here"
        echo "GOOGLE_API_KEY=your_google_api_key_here"
        exit 1
    fi
    log_info ".env file found"
}

# Build the Docker image
build() {
    log_info "Building GruntBot Docker image..."
    docker-compose build
    log_info "Build completed successfully!"
}

# Start the bot
start() {
    check_env
    log_info "Starting GruntBot..."
    docker-compose up -d
    log_info "GruntBot is now running in the background!"
    log_info "Use 'docker-compose logs -f gruntbot' to view logs"
}

# Stop the bot
stop() {
    log_info "Stopping GruntBot..."
    docker-compose down
    log_info "GruntBot stopped"
}

# Restart the bot
restart() {
    log_info "Restarting GruntBot..."
    docker-compose restart
    log_info "GruntBot restarted"
}

# View logs
logs() {
    docker-compose logs -f gruntbot
}

# Update and restart
update() {
    log_info "Updating GruntBot..."
    git pull origin main
    build
    stop
    start
    log_info "GruntBot updated and restarted!"
}

# Show status
status() {
    docker-compose ps
}

# Clean up
clean() {
    log_warn "This will remove the GruntBot container and image"
    read -p "Are you sure? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        docker-compose down --rmi all --volumes
        log_info "Cleanup completed"
    else
        log_info "Cleanup cancelled"
    fi
}

# Help
help() {
    echo "GruntBot Docker Management Script"
    echo ""
    echo "Usage: $0 {build|start|stop|restart|logs|update|status|clean|help}"
    echo ""
    echo "Commands:"
    echo "  build   - Build the Docker image"
    echo "  start   - Start GruntBot in the background"
    echo "  stop    - Stop GruntBot"
    echo "  restart - Restart GruntBot"
    echo "  logs    - View live logs"
    echo "  update  - Pull latest code and restart"
    echo "  status  - Show container status"
    echo "  clean   - Remove containers and images"
    echo "  help    - Show this help message"
}

# Main script logic
case "${1:-help}" in
    build)
        build
        ;;
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    logs)
        logs
        ;;
    update)
        update
        ;;
    status)
        status
        ;;
    clean)
        clean
        ;;
    help|*)
        help
        ;;
esac
