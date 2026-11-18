# Setup Instructions

This repository automatically updates the README.md with:
- Current weather information for Berkeley, CA
- Sunrise and sunset times
- A random image from the Digital Abstract or Low CFG Series pages on benjifriedman.com

## Local Development

1. Copy `secrets.ini.example` to `secrets.ini`:
   ```bash
   cp secrets.ini.example secrets.ini
   ```

2. Fill in your API credentials in `secrets.ini`:
   - OpenWeather API key from https://openweathermap.org/api

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the script:
   ```bash
   python main.py
   ```

## GitHub Actions Setup

The README updates automatically every hour via GitHub Actions.

### Required GitHub Secrets

Add these secrets to your repository (Settings → Secrets and variables → Actions):

- `openweather_api_key` - Your OpenWeather API key

### Manual Trigger

You can manually trigger the workflow from the Actions tab → Update README → Run workflow.

## How It Works

- `main.py` - Main script that fetches data and generates README
- `infrastructure/weather.py` - Fetches weather data from OpenWeather API
- `infrastructure/website_image.py` - Picks a random image from the Digital Abstract or Low CFG Series pages on benjifriedman.com
- `templates/main.html` - Jinja2 template for the README
- `.github/workflows/update-readme.yml` - GitHub Actions workflow
