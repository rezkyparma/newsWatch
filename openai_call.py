import openai
import IPython
import json
import time
from langchain.llms import OpenAI
import csv

with open("constant.txt", 'r') as const:
    key = const.read().strip()
    print(key)

openai.api_key = "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"

def set_open_params(
        model="gpt-3.5-turbo",
        temperature=0.0,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
):
    """ set openai parameters"""

    openai_params = {}
    openai_params['model'] = model
    openai_params['temperature'] = temperature
    openai_params['max_tokens'] = max_tokens
    openai_params['top_p'] = top_p
    openai_params['frequency_penalty'] = frequency_penalty
    openai_params['presence_penalty'] = presence_penalty
    return openai_params


# Feed prompt and params to the OpenAI model and return response
def get_chat_completion(params, prompt, delay=0):
    """ GET completion from openai api"""

    response = openai.ChatCompletion.create(
        model=params['model'],
        messages=[
            {'role': 'user', 'content': prompt}
        ],
        temperature=params['temperature'],
        max_tokens=params['max_tokens'],
        top_p=params['top_p'],
        frequency_penalty=params['frequency_penalty'],
        presence_penalty=params['presence_penalty'],
    )
    # delay to keep within rate limit
    time.sleep(delay)
    return response.choices[0]['message']['content']


class ArticleEvaluate:
    def __init__(self, url):
        self.input_url = url

    def get_info(self):
        prompt = f"""
        Identify the following items from the url,Format your response as a JSON object with \
        key value pair: 
        - subject: Who is the subject present in the article, if more than one subject apply in python list
        - summary: What is the article pointing out
        - category: What is the general category of this article
        - sub category: What is the subcategory of this article
        - keyword: What is the most used keyword in this article, if multiple result apply in python list
        - related keyword: suggest related keyword for this article, that can be used to optimise SEO for competing article, if multiple result apply in python list
        - suggestion article: suggest article title to compete with this article based on related keyword, applying long tail keyword
        
        The url is delimited with triple backticks. \
        
        If the information isn't present, use "unknown" \
        as the value.
        Make your response as short as possible in indonesian language.
        
        Review text: ```{self.input_url}```
        """

        params = set_open_params(temperature=1)
        response = get_chat_completion(params, prompt)

        with open('information-extraction.txt', 'a', newline='\n') as file:
            file.writelines(f'------------------\r\nPrompt:{prompt}\r\n-- Temperature:{params["temperature"]}\r\n-- '
                            f'Result:\r\n{response}\r\n \r\n')
        return response

