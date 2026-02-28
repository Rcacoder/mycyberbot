# Cyber Attack Reporter and Lesson Generator

A Python-based application that automatically fetches the latest cybersecurity news from reputable RSS feeds, uses the DeepSeek API to analyze and extract the Top 10 global threats, and generates customized academic teaching lessons for the Top 2 incidents. 

The system features:
1. **Automated Aggregation**: Continuous fetching via `feedparser`.
2. **AI Intelligence**: DeepSeek-powered analysis and lesson planning.
3. **Email Notifications**: Scheduled HTML email reporting via SMTP.
4. **Interactive Dashboard**: A beautiful, dark-mode glassmorphism Web UI built with FastAPI.

## Prerequisites
- Python 3.10+
- DeepSeek API Key
- Gmail App Password (or other SMTP credentials) for notifications

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Rcacoder/mycyberbot.git
cd mycyberbot
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Mac/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

3. Configure your Environment Variables:
Create a `.env` file in the root directory:
```env
DEEPSEEK_API_KEY=your_deepseek_api_key
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
RECEIVER_EMAIL=your_email@gmail.com
```

## Usage

### Run the Core Data Pipeline
To manually run the pipeline, fetch the news, analyze the data, and generate the daily report JSON:
```bash
python main.py
```
*(Use `--dry-run` to test the output in the console without sending an email).*

### Launch the Web Dashboard
After running the pipeline at least once to generate a report, you can view the historical data on the premium web interface:
```bash
python server.py
```
Then navigate to `http://localhost:8000/app` in your browser.

## Automation
For daily operation, schedule `main.py` using Windows Task Scheduler or a Linux CRON job to run automatically every morning.

## Architecture
- `fetcher.py`: Manages RSS Feeds
- `analyzer.py`: Handles deep API integrations with DeepSeek
- `notifier.py`: Builds and sends HTML emails
- `main.py`: Orchestrates the daily flow
- `server.py`: Serves the FastAPI web interface
- `web/`: Contains the Glassmorphism CSS, HTML, and JS logic
