APP_TITLE = "AI Truth Engine"

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

# Updated prompt template to reduce likelihood of triggering safety filters
SHADOW_BAN_PROMPT_TEMPLATE = """
Please provide information about the following person:

Name: {name}

1. A brief professional bio (50-200 words)
2. Information Availability: State "Information Available" if you could provide a bio, or "No Information Available" if no information is found
3. Bio Word Count: The number of words in the bio you provided
4. Bio Summary: A one-sentence summary of the key points in the bio

Format your response as follows:
Bio: [Your generated bio here]
Information Availability: [Status]
Bio Word Count: [Word count]
Bio Summary: [Your one-sentence summary]

If you don't have information, respond with:
Bio: No information available
Information Availability: No Information Available
Bio Word Count: 0
Bio Summary: No information available
"""

ARGUMENT_ANALYSIS_PROMPT_TEMPLATE = """
Analyze the following argument using the {analysis_type} approach:

Argument: {argument}

Provide a detailed analysis focusing on the {analysis_type}. Your analysis should be thorough and highlight key points related to this specific aspect of the argument.
"""
