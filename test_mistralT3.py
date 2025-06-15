import requests
import pandas as pd
import json

df = pd.read_csv("products_dropshippingT3.csv", sep=';')

prompt_header = (
    "You are a dropshipping assistant. Choose the best products from products listed below.\n"
    "Make separte list for ones you rejected. Make space between each product\n"
    "Criteria: more than 50,000 Google searches, low TikTok popularity (the lower the better), low competition, margin over 3.0.\n"
    "Mark which products are suitable and which not. Justify each decision clearly.\n\n"
)

product_lines = []
for _, row in df.iterrows():
    line = f"- {row['Name']} | Google: {row['Google_searches']} | TikTok: {row['Tiktok_popularity']} | Competition: {row['Competition_level']} | Margin: {row['Margin']}"
    product_lines.append(line)

full_prompt = prompt_header + "\n".join(product_lines)

response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "mistral",
        "prompt": full_prompt,
        "temperature": 0.1
    },
    stream=True
)

print("\n Model response:\n")
for line in response.iter_lines():
    if line:
        decoded_line = json.loads(line.decode("utf-8"))
        if "response" in decoded_line:
            print(decoded_line["response"], end="", flush=True)
