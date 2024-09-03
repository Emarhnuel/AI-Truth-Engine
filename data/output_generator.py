import pandas as pd
import io


def generate_excel(results, filename):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        if isinstance(results, dict):
            for llm, data in results.items():
                if isinstance(data, str):
                    # If data is a string, create a single-column DataFrame
                    df = pd.DataFrame({llm: [data]})
                elif isinstance(data, (list, dict)):
                    # If data is a list or dict, create a DataFrame
                    df = pd.DataFrame(data)
                else:
                    # If data is neither string nor list/dict, skip it
                    continue

                # Ensure the sheet name is valid for Excel
                sheet_name = str(llm)[:31].replace('[', '').replace(']', '').replace(':', '')
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        else:
            # If results is not a dict, create a single sheet with all data
            pd.DataFrame(results).to_excel(writer, sheet_name='Results', index=False)

    output.seek(0)
    return output.getvalue()


def generate_csv(results, filename):
    output = io.StringIO()
    for llm, data in results.items():
        df = pd.DataFrame(data)
        df.to_csv(output, index=False)
        output.write("\n")  # Add a blank line between LLM results
    return output.getvalue()
