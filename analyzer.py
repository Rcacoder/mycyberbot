import os
import json
import logging
from typing import List, Dict, Any
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize OpenAI client pointed to DeepSeek API
api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key or api_key == "your_deepseek_api_key_here":
    logging.warning("DEEPSEEK_API_KEY is not set or is using the default placeholder.")

client = OpenAI(
    api_key=api_key if api_key else "dummy_key_for_testing",
    base_url="https://api.deepseek.com/v1"
)

MODEL_NAME = "deepseek-chat"

def analyze_news(articles: List[Dict[str, str]]) -> Dict[str, Any]:
    """
    Uses DeepSeek to:
    1. Select the top 10 most impactful cyber attacks from the article list.
    2. Generate a teaching lesson for the top 2 attacks.
    """
    if not articles:
        return {"top_10_attacks": [], "lessons": []}
        
    logging.info(f"Sending {len(articles)} articles to DeepSeek for analysis...")
    
    # Prepare the prompt
    articles_json = json.dumps(articles, indent=2)
    
    system_prompt = """
You are an expert cybersecurity professor and analyst.
You will be provided with a daily feed of cybersecurity news articles in JSON format.
Your task is to analyze these articles and output a strictly formatted JSON response.

Instructions:
1. Review all the provided articles.
2. Select the "Top 10" most impactful, severe, or notable cyber attacks/threats from the list.
3. For the top 2 out of those 10, generate a brief teaching lesson suitable for university students.

The output MUST be valid JSON matching this exact structure:
{
  "top_10_attacks": [
    {
      "rank": 1,
      "title": "Title of the attack/article",
      "source": "Source Name",
      "link": "https://...",
      "summary": "1-2 sentence summary of why this is impactful"
    },
    ...
  ],
  "lessons": [
    {
      "rank": 1,
      "title": "Title of the attack",
      "learning_objectives": ["Objective 1", "Objective 2"],
      "real_world_impact": "Explanation of the impact.",
      "mitigation_strategies": ["Strategy 1", "Strategy 2"],
      "discussion_questions": ["Question 1", "Question 2"]
    },
    {
      "rank": 2,
      ...
    }
  ]
}
Return ONLY the raw JSON format, without markdown blocks, preambles, or postscripts.
"""
    
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Daily News Feed:\n{articles_json}"}
            ],
            temperature=0.3,
        )
        
        reply_text = response.choices[0].message.content.strip()
        
        # Strip potential markdown formatting if the model still includes it
        if reply_text.startswith("```json"):
            reply_text = reply_text[7:]
        if reply_text.endswith("```"):
            reply_text = reply_text[:-3]
            
        result_data = json.loads(reply_text.strip())
        return result_data
        
    except Exception as e:
        logging.error(f"Error communicating with DeepSeek API or parsing response: {e}")
        return {"top_10_attacks": [], "lessons": []}

if __name__ == "__main__":
    # Simple mock test
    # We won't actually call the API here because it requires a valid key, 
    # but we can print a success message that it's imported correctly.
    print("Analyzer module ready.")
