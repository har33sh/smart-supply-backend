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

os.environ["OPENROUTER_API_KEY"] = OPEN_ROUTER_API

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=OPEN_ROUTER_API,
)

def analyze_email_with_openrouter(email_text):
    """
    Analyzes email text using OpenRouter API to extract information in a JSON format.

    Args:
        email_text: The input email text as a string.

    Returns:
        A JSON formatted string containing the extracted information.
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

    response = client.chat.completions.create(
      model="deepseek/deepseek-r1-0528:free",  # You can choose a specific model here
      messages=[
        {"role": "user", "content": prompt},
      ],
      response_format={"type": "json_object"},
    )

    return json.dumps(json.loads(response.choices[0].message.content), indent=2)

# # Input text
# input_text = "dispatch@tirupurmart.in,\"Hi Sir, Fabric quality is not matching as per sample given. Please advise what to do.\""


# # Analyze the email content
# json_output = analyze_email_with_openrouter(input_text)

# # Print the JSON output
# print(json_output)
