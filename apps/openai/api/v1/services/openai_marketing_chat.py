import openai
from core import settings


def chat_with_gpt(input):

    openai.api_key = settings.OPENAI_API_KEY

    TEMPLATE_PROMPT = f"Generate a content post for a company called {input.get('company', None)}. \n "
    f"This is the companies bio information: {input.get('bio_information', None)}. \n"
    f"The post should focus on the following theme keywords: {input.get('keywords', None)}. \n"
    f"The subject or tone of the content should be {input.get('tone', None)}. \n"
    f"The output should be formatted for a {input.get('output_format', None)} and should be seperated by paragraphs. \n"

    HASHTAGS = f"\n {input.get('hashtags', None)}. \n"

    try:
        print("calling chatgpt")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": str(TEMPLATE_PROMPT)}])
        message = response.choices[0].message.content
        return str(message) + str(HASHTAGS)
    except Exception as e:
        print("error in chatgpt", e)
        return str(e)
