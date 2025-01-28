
import json
import re
import pandas as pd
from openai import OpenAI
import yaml

api_key = None
CONFIG_PATH = r"config.yaml"

with open(CONFIG_PATH) as file:
    data = yaml.load(file, Loader=yaml.FullLoader)
    api_key = data['DEEPSEEK_KEY']

def details_extractor(resume_data):

    prompt = '''
    You are an AI bot designed to act as a professional for parsing resumes. You are given with resume and your job is to extract the following information from the resume:
    1. full name
    2. email id
    3. gender
    4. age as of 2009
    5. phone
    6. C.G.P.A
    7. Branch
    8. State mentioned in permanent address
    9. City mentioned in permanent address
    10.INSTITUTION in xth
    11.INSTITUTION in XIIth
    11.Marks in xth
    12.Marks in XIIth
    13.employment details
    14.technical skills
    15.soft skills
    16.sports
    17.research experience
    Give the extracted information in json format only. key names in the json has to be same as mentioned in this promt always.
    '''
    messages=[{"role": "system","content": prompt}]
    messages.append({"role": "user", "content": resume_data})

    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    response = client.chat.completions.create(
    model="deepseek-chat",
    messages=messages,
    stream=False
)

    # print(response.choices[0].message.content)

    text=response.choices[0].message.content
    json_str=""
    
    pattern = r"```json\n\s*(.*?)\s*```"
    match = re.search(pattern, text, re.DOTALL)
    if match: 
        json_str = match.group(1) 
        # print("Extracted JSON:") 
        # print(json_str) 
    else: 
        print("No JSON data found.")
    

    data_dict = json.loads(json_str)
    # Normalize the dictionary to handle nested structures
    details = pd.json_normalize(data_dict, sep='_')

    return details