import openai
import settings


def chat_with_gpt(input):

    openai.api_key = settings.OPENAI_API_KEY

    TEMPLATE_PROMPT = f"Generate a content post for a company called {input.get('company', None)}. \n "
    f"This is the companies bio information: {input.get('bio_information', None)}. \n"
    f"The post should focus on the following theme keywords: {input.get('keywords', None)}. \n"
    f"The subject or tone of the content should be {input.get('tone', None)}. The output should be formatted for a {input.get('output_format', None)}. \n"
    # "Include emojis and hashtags in the output. \n"
    # "Format the output as paragraphs. \n"

    print("calling chatgpt")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": str(TEMPLATE_PROMPT)}])
    message = response.choices[0].message.content
    return message
