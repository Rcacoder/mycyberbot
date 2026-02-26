import argparse
import logging
import json
import os
from datetime import datetime
from fetcher import fetch_daily_news
from analyzer import analyze_news
from notifier import generate_html_report, send_email_report

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    parser = argparse.ArgumentParser(description="Daily Cyber Attack Reporter and Lesson Generator")
    parser.add_argument("--dry-run", action="store_true", help="Print the report to the console instead of emailing it")
    parser.add_argument("--save-json", action="store_true", help="Save the DeepSeek response to a local JSON file")
    args = parser.parse_args()

    # Step 1: Fetch Articles
    logging.info("Starting Daily Cyber Attack Reporter")
    articles = fetch_daily_news()
    
    if not articles:
        logging.info("No articles found in the last 24 hours. Exiting.")
        return

    # Step 2: Analyze with DeepSeek
    logging.info("Analyzing articles with DeepSeek API...")
    if not os.getenv("DEEPSEEK_API_KEY") or os.getenv("DEEPSEEK_API_KEY") == "your_deepseek_api_key_here":
        logging.error("Valid DEEPSEEK_API_KEY is required to proceed.")
        return
        
    analysis_result = analyze_news(articles)
    
    if not analysis_result or not analysis_result.get("top_10_attacks"):
        logging.warning("DeepSeek API did not return any attacks. Exiting.")
        return

    # Step 3: Handle Results
    # Save JSON Report for the Web UI everyday
    date_str = datetime.now().strftime("%Y-%m-%d")
    report_path = os.path.join("reports", f"{date_str}.json")
    
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(analysis_result, f, indent=2)
    logging.info(f"Daily analysis saved to {report_path} for Web UI")
    
    if args.save_json:
        with open("last_report.json", "w", encoding="utf-8") as f:
            json.dump(analysis_result, f, indent=2)
        logging.info("Analysis also saved to last_report.json")

    if args.dry_run:
        logging.info("DRY RUN MODE ENABLED. Generating HTML but not sending email.")
        html = generate_html_report(analysis_result)
        
        # Save HTML to a file so it can be viewed locally
        with open("dry_run_report.html", "w", encoding="utf-8") as f:
            f.write(html)
        logging.info("Dry run HTML report saved to dry_run_report.html")
        
        # Also print a summary to console
        print("\n--- DRY RUN SUMMARY ---")
        for idx, attack in enumerate(analysis_result.get("top_10_attacks", [])):
            print(f"{idx+1}. {attack.get('title')}")
        print("-----------------------")
    else:
        logging.info("Sending email report...")
        
        # Replace the `send_email_report` functionality internally with the actual implementation
        # For security, the user must update their .env variables
        send_email_report(analysis_result)
        
    logging.info("Process completed successfully.")

if __name__ == "__main__":
    main()
