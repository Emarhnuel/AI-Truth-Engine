from llm_interface import get_llm, query_llm
from config import SHADOW_BAN_PROMPT_TEMPLATE
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import logging
import pandas as pd

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Download necessary NLTK data
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
except Exception as e:
    logger.warning(f"Failed to download NLTK data: {str(e)}")

def check_shadow_ban(df, selected_llms, llm_api_keys):
    results = {llm: [] for llm in selected_llms}

    for _, row in df.iterrows():
        name = row['Names']
        for llm_name in selected_llms:
            try:
                llm = get_llm(llm_name, llm_api_keys.get(llm_name))
                response = query_llm(llm, SHADOW_BAN_PROMPT_TEMPLATE, name=name)

                if response.startswith("Error:"):
                    parsed_response = {
                        "Information Availability": "Error",
                        "Bio Word Count": "0",
                        "Confidence Score": "0",
                        "Bio Summary": response
                    }
                else:
                    parsed_response = parse_llm_response(response)

                result = {
                    "Name": name,
                    "LLM": llm_name,
                    "Information Availability": parsed_response.get("Information Availability", "Unknown"),
                    "Bio Word Count": parsed_response.get("Bio Word Count", "0"),
                    "Confidence Score": parsed_response.get("Confidence Score", "0"),
                    "Bio Summary": parsed_response.get("Bio Summary", "No summary available")
                }
                results[llm_name].append(result)
            except Exception as e:
                logging.error(f"Error processing {name} with {llm_name}: {str(e)}")
                results[llm_name].append({
                    "Name": name,
                    "LLM": llm_name,
                    "Information Availability": "Error",
                    "Bio Word Count": "0",
                    "Confidence Score": "0",
                    "Bio Summary": f"Error: {str(e)}"
                })

    return results

def parse_llm_response(response):
    lines = response.strip().split('\n')
    parsed_response = {}
    for line in lines:
        if ':' in line:
            key, value = line.split(':', 1)
            parsed_response[key.strip()] = value.strip()
    return parsed_response

def calculate_bias_score(user_actions):
    weights = {
        'reports': 2,
        'offensive_words': 3,
        'spam_messages': 1,
        'positive_interactions': -1
    }
    return sum(weights.get(action, 0) * count for action, count in user_actions.items())

def summarize_bio(bio):
    try:
        words = word_tokenize(bio)
        stop_words = set(stopwords.words('english'))
        filtered_words = [word for word in words if word.lower() not in stop_words]

        if len(filtered_words) <= 90:
            return ' '.join(filtered_words)

        summary = ' '.join(filtered_words[:90])
        return summary + '...' if len(summary) < len(bio) else summary
    except Exception as e:
        logger.warning(f"Error in summarizing bio: {str(e)}. Falling back to simple summarization.")
        return simple_summarize(bio)

def simple_summarize(bio):
    words = bio.split()
    return ' '.join(words[:90]) + '...' if len(words) > 90 else bio
