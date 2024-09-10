import pandas as pd
import io

def generate_excel(results, filename):
    output = io.BytesIO()
    
    data = []
    for name in results[list(results.keys())[0]]:
        row = {'Name': name['Name']}
        for llm, llm_results in results.items():
            llm_result = next(r for r in llm_results if r['Name'] == name['Name'])
            status = 'Shadow Banned' if llm_result['Score'] == 0 else 'Not Shadow Banned'
            row[f"{llm} Score"] = llm_result['Score']
            row[f"{llm} Status"] = status
        data.append(row)
    
    df = pd.DataFrame(data)
    df.to_excel(output, index=False, sheet_name='Shadow Ban Results')
    
    output.seek(0)
    return output.getvalue()
