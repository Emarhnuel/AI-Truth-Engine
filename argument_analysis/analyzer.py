from llm_interface import get_llm, query_llm
from config import ARGUMENT_ANALYSIS_PROMPT_TEMPLATE

def analyze_argument(argument, analysis_types, selected_llms, llm_api_keys):
    results = {}
    for llm_name in selected_llms:
        llm = get_llm(llm_name, llm_api_keys.get(llm_name))
        results[llm_name] = {}
        for analysis_type in analysis_types:
            results[llm_name][analysis_type] = query_llm(
                llm,
                ARGUMENT_ANALYSIS_PROMPT_TEMPLATE,
                argument=argument,
                analysis_type=analysis_type
            )
    return results
