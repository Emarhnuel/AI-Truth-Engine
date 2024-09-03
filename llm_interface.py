from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI, ChatAnthropic
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import google.generativeai as genai
from groq import Groq
from config import LLM_CONFIGS

def get_llm(llm_name, api_key):
    config = LLM_CONFIGS[llm_name]
    if config["class"] == "ChatOpenAI":
        return ChatOpenAI(model_name=config["model_name"], api_key=api_key)
    elif config["class"] == "ChatAnthropic":
        return ChatAnthropic(model=config["model_name"], api_key=api_key)
    elif config["class"] == "Gemini":
        genai.configure(api_key=api_key)
        return genai.GenerativeModel(config["model_name"])
    elif config["class"] == "Groq":
        return (Groq(api_key=api_key), config["model_name"])
    else:
        raise ValueError(f"Unsupported LLM: {llm_name}")

def query_llm(llm, prompt_template, **kwargs):
    prompt = PromptTemplate(template=prompt_template, input_variables=list(kwargs.keys()))
    if isinstance(llm, genai.GenerativeModel):
        response = llm.generate_content(prompt.format(**kwargs))
        return response.text
    elif isinstance(llm, tuple) and isinstance(llm[0], Groq):
        groq_instance, model_name = llm
        response = groq_instance.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt.format(**kwargs)}]
        )
        return response.choices[0].message.content
    else:
        chain = LLMChain(llm=llm, prompt=prompt)
        return chain.run(**kwargs)