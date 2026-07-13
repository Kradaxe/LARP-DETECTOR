from google import genai

client = genai.Client(api_key="AQ.Ab8RN6KQ_mFAt-vCbrYu1ENlffh1hgzm591CwnYGDRWWcjDbXg")

for model in client.models.list():
    print(model.name)