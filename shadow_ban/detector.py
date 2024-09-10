from llm_interface import get_llm, query_llm_batch
import pandas as pd
import concurrent.futures
import re

def process_batch(batch, selected_llms, llm_api_keys):
    batch_results = {llm: [] for llm in selected_llms}
    for llm_name in selected_llms:
        llm = get_llm(llm_name, llm_api_keys.get(llm_name))
        names = batch['Names'].tolist()
        prompt = """For the person named {name}:
1. Determine if they are shadow banned. A person is considered shadow banned if there is no publicly available information about them or if their online presence seems artificially limited.
2. On a scale of 0 to 100, how prominent or famous is this individual?

Respond in the following format:
Shadow Banned: [Yes/No]
Prominence Score: [0-100]

If the person is shadow banned, set the Prominence Score to 0. If not shadow banned, the score should be at least 1."""

        responses = query_llm_batch(llm, prompt, names)
        
        for name, response in zip(names, responses):
            shadow_banned = False
            score = 0
            
            # Use regex to find shadow ban status and score
            shadow_ban_match = re.search(r'Shadow\s*Banned:\s*(Yes|No)', response, re.IGNORECASE)
            score_match = re.search(r'Prominence\s*Score:\s*(\d+)', response, re.IGNORECASE)
            
            if shadow_ban_match:
                shadow_banned = shadow_ban_match.group(1).lower() == 'yes'
            
            if score_match:
                score = int(score_match.group(1))
            
            # Ensure consistency between shadow ban status and score
            if shadow_banned:
                score = 0
            elif score == 0:
                score = 1  # Minimum score for not shadow banned
            
            batch_results[llm_name].append({
                "Name": name,
                "Shadow Banned": shadow_banned,
                "Score": score
            })
    
    return batch_results

def check_shadow_ban_parallel(df, selected_llms, llm_api_keys, batch_size=100, max_workers=5):
    results = {llm: [] for llm in selected_llms}

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for i in range(0, len(df), batch_size):
            batch = df.iloc[i:i+batch_size]
            futures.append(executor.submit(process_batch, batch, selected_llms, llm_api_keys))

        for future in concurrent.futures.as_completed(futures):
            batch_results = future.result()
            for llm_name, llm_results in batch_results.items():
                results[llm_name].extend(llm_results)

    return results
