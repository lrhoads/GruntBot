# GruntBot Docker Setup

This directory contains Docker configuration for running GruntBot in a containerized environment.

## Prerequisites

- Docker and Docker Compose installed
- `.env` file with your API keys

## Quick Start

1. **Create your `.env` file:**
   ```bash
   cp .env.example .env
   # Edit .env with your actual API keys
   ```

2. **Build and start the bot:**
   ```bash
   chmod +x grunt-docker.sh
   ./grunt-docker.sh start
   ```

## Docker Commands

### Using the management script (recommended):
```bash
./grunt-docker.sh build     # Build the Docker image
./grunt-docker.sh start     # Start GruntBot
./grunt-docker.sh stop      # Stop GruntBot
./grunt-docker.sh restart   # Restart GruntBot
./grunt-docker.sh logs      # View live logs
./grunt-docker.sh update    # Pull latest code and restart
./grunt-docker.sh status    # Show container status
./grunt-docker.sh clean     # Remove containers and images
```

### Using Docker Compose directly:
```bash
# Build the image
docker-compose build

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f gruntbot

# Stop
docker-compose down

# Restart
docker-compose restart
```

## Environment Variables

Required in your `.env` file:
- `DISCORD_TOKEN` - Your Discord bot token
- `GOOGLE_API_KEY` - Your Google Generative AI API key

## Persistent Data

The following directories are mounted as volumes to persist data:
- `./res/` - Contains profiles.json and other resource files
- `./logs/` - Container logs (optional)

## Resource Limits

The container is configured with:
- Memory limit: 512MB
- CPU limit: 0.5 cores
- Memory reservation: 256MB
- CPU reservation: 0.25 cores

## Deployment on Server

1. **Clone the repository:**
   ```bash
   git clone https://github.com/lrhoads/GruntBot.git
   cd GruntBot
   ```

2. **Set up environment:**
   ```bash
   cp .env.example .env
   nano .env  # Add your API keys
   ```

3. **Start the bot:**
   ```bash
   chmod +x grunt-docker.sh
   ./grunt-docker.sh start
   ```

4. **To update later:**
   ```bash
   ./grunt-docker.sh update
   ```

## Monitoring

- View real-time logs: `./grunt-docker.sh logs`
- Check status: `./grunt-docker.sh status`
- Container will automatically restart unless manually stopped

## Troubleshooting

- **Bot not starting**: Check logs with `./grunt-docker.sh logs`
- **Permission denied**: Make sure script is executable: `chmod +x grunt-docker.sh`
- **Environment issues**: Verify your `.env` file has the correct API keys
- **Build issues**: Try `./grunt-docker.sh clean` then `./grunt-docker.sh build`
