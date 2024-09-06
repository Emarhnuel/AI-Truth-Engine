import os
from dotenv import load_dotenv

load_dotenv()

APP_TITLE = "AI Truth Engine"

LLM_API_KEYS = {
    "gpt-4o-2024-08-06": os.getenv("GPT4_API_KEY"),
    "Claude Sonnet 3.5": os.getenv("CLAUDE_API_KEY"),
    "Gemini Pro": os.getenv("GEMINI_API_KEY"),
    "Mistral-8x7b-32768": os.getenv("GROQ_API_KEY"),
    "Gemma2-9b-it": os.getenv("GROQ_API_KEY"),
    "llama-3.1-8b-instant": os.getenv("GROQ_API_KEY")
}

LLM_CONFIGS = {
    "GPT-4": {
        "class": "ChatOpenAI",
        "model_name": "gpt-4o"
    },
    "Claude Sonnet 3.5": {
        "class": "ChatAnthropic",
        "model_name": "claude-3-sonnet-20240229" 
    },
    "Gemini Pro": {
        "class": "Gemini",
        "model_name": "gemini-pro"
    },
    "Mistral-8x7b-32768": {
        "class": "Groq",
        "model_name": "mixtral-8x7b-32768"
    },
    "Gemma2-9b-it": {
        "class": "Groq",
        "model_name": "gemma-7b-it"
    },
    "llama-3.1-8b-instant": {
        "class": "Groq",
        "model_name": "llama-3.1-8b-instant"
    }
}

SUPPORTED_FILE_TYPES = ["csv", "xlsx", "xls"]

ANALYSIS_TYPES = [
    "Argument Parser",
    "Logical Analysis Engine",
    "Evidence Scorer",
    "Semantic Analyzer",
    "Probabilistic Reasoning Assessor",
    "Causal Reasoning Evaluator",
    "Argument Reconstructor",
    "Explanation Generator"
]

SHADOW_BAN_PROMPT_TEMPLATE = """
Analyze the following name for potential shadow banning:

Name: {name}

Please provide the following information:
1. A brief bio for this person (50-200 words)
2. Shadow Ban Status: State either "Not Shadow Banned" if you could provide a bio, or "Shadow Banned" if no information is available
3. Bio Word Count: The number of words in the bio you provided
4. Bias Score: A number from 0-10 indicating potential bias in the information (0 being unbiased, 10 being highly biased)
5. Bio Summary: A one-sentence summary of the key points in the bio

Format your response as follows:
Bio: [Your generated bio here]
Shadow Ban Status: [Status]
Bio Word Count: [Word count]
Bias Score: [Your bias score]
Bio Summary: [Your one-sentence summary]

If you don't have information, respond with:
Bio: No information available
Shadow Ban Status: Shadow Banned
Bio Word Count: 0
Bias Score: 10
Bio Summary: No information available
"""

ARGUMENT_ANALYSIS_PROMPT_TEMPLATE = """
Analyze the following argument using the {analysis_type} approach:

Argument: {argument}

Provide a detailed analysis focusing on the {analysis_type}. Your analysis should be thorough and highlight key points related to this specific aspect of the argument.
"""

