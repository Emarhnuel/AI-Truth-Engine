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
            llm = get_llm(llm_name, llm_api_keys.get(llm_name))
            response = query_llm(llm, SHADOW_BAN_PROMPT_TEMPLATE, name=name)

            # Parse the response
            parsed_response = parse_llm_response(response)

            result = {
                "Name": name,
                "LLM": llm_name,
                "Shadow Ban Status": parsed_response.get("Shadow Ban Status", "Unknown"),
                "Bio Word Count": parsed_response.get("Bio Word Count", "0"),
                "Bias Score": parsed_response.get("Bias Score", "0"),
                "Bio Summary": parsed_response.get("Bio Summary", "No summary available")
            }
            results[llm_name].append(result)

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
    # Define weights for different actions
    weights = {
        'reports': 2,
        'offensive_words': 3,
        'spam_messages': 1,
        'positive_interactions': -1
    }

    # Initialize bias score
    bias_score = 0

    # Calculate weighted sum
    for action, count in user_actions.items():
        if action in weights:
            bias_score += weights[action] * count

    return bias_score


# Example usage
user_actions = {
    'reports': 5,
    'offensive_words': 3,
    'spam_messages': 10,
    'positive_interactions': 20
}

score = calculate_bias_score(user_actions)
print(f"Bias Score: {score}")


def summarize_bio(bio):
    try:
        words = word_tokenize(bio)
        stop_words = set(stopwords.words('english'))
        filtered_words = [word for word in words if word.lower() not in stop_words]

        if len(filtered_words) <= 90:
            return ' '.join(filtered_words)

        summary = ' '.join(filtered_words[:90])

        if len(summary) < len(bio):
            summary += '...'

        return summary
    except Exception as e:
        logger.warning(f"Error in summarizing bio: {str(e)}. Falling back to simple summarization.")
        return simple_summarize(bio)

def simple_summarize(bio):
    words = bio.split()
    if len(words) <= 90:
        return bio
    return ' '.join(words[:90]) + '...'
