# prompt: you have text like this. 
# 40,Email,dispatch@tirupurmart.in,"Hi Sir, Fabric quality is not matching as per sample given. Please advise what to do."
# take it as input. send to openrouter api. 
# return json formateed data
# email
# status: completed|ongoing|delayed|
# advise_required: yes|no
# eta:
# and other fields


import os
import json
from openai import OpenAI
from typing import Optional

def get_openrouter_client(api_key: Optional[str] = None):
    api_key = api_key or os.getenv("OPEN_ROUTER_API")
    if not api_key:
        raise ValueError("OPEN_ROUTER_API is not set.")
    return OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

def analyze_email_with_openrouter(email_text, api_key: Optional[str] = None):
    """
    Analyzes email text using OpenRouter API to extract information in a JSON format.
    Args:
        email_text: The input email text as a string.
        api_key: Optional API key to override environment variable.
    Returns:
        A dict containing the extracted information.
    """
    prompt = f"""Analyze the following email text and extract the following information in a JSON format:
    email: The email address mentioned in the text.
    status: Determine the status of the issue mentioned in the email. Possible values: completed|In Production|Ready to Ship|Partial|.
    flag_type: delay, quality_issue, payment_block, logistics, partial, other
    other_fields: Any other relevant information from the email that needs review
    eta: If an Estimated Time of Arrival (ETA) is mentioned or can be inferred, provide it. Otherwise, leave it empty.

    Email Text:
    {email_text}

    Return only the JSON object, no extra text.
    """
    client = get_openrouter_client(api_key)
    response = client.chat.completions.create(
        model="deepseek/deepseek-r1-0528:free",
        messages=[
            {"role": "user", "content": prompt},
        ],
        response_format={"type": "json_object"},
    )


    return json.loads(response.choices[0].message.content)

# # Input text
# input_text = "dispatch@tirupurmart.in, Hi Sir, Fabric quality is not matching as per sample given. Please advise what to do.""


# # Analyze the email content
# json_output = analyze_email_with_openrouter(input_text)

# # Print the JSON output
# print(json_output)

