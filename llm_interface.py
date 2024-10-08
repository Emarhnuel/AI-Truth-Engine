from langchain.chat_models import ChatOpenAI, ChatAnthropic
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import google.generativeai as genai
from groq import Groq
from config import LLM_CONFIGS
from langchain_anthropic import ChatAnthropic

def get_llm(llm_name, api_key):
    config = LLM_CONFIGS.get(llm_name)
    if not config:
        raise ValueError(f"Unsupported LLM: {llm_name}")

    if config["class"] == "ChatAnthropic":
        return ChatAnthropic(model=config["model_name"], anthropic_api_key=api_key)
    elif config["class"] == "ChatOpenAI":
        return ChatOpenAI(model=config["model_name"], openai_api_key=api_key)
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
        if not response.parts:
            raise ValueError("The response was blocked. Please check the safety ratings.")
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

def query_llm_batch(llm, prompt_template, names):
    prompts = [PromptTemplate(template=prompt_template, input_variables=["name"]).format(name=name) for name in names]
    
    if isinstance(llm, genai.GenerativeModel):
        responses = [llm.generate_content(prompt) for prompt in prompts]
        return [r.text for r in responses if r.parts]
    elif isinstance(llm, tuple) and isinstance(llm[0], Groq):
        groq_instance, model_name = llm
        responses = []
        for prompt in prompts:
            response = groq_instance.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}]
            )
            responses.append(response.choices[0].message.content)
        return responses
    else:
        chain = LLMChain(llm=llm, prompt=PromptTemplate(template=prompt_template, input_variables=["name"]))
        results = chain.apply([{"name": name} for name in names])
        return [result['text'] for result in results]
