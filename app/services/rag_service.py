from openai import OpenAI
import os

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

def generate_answer(question, content_chunks):
    print('come later')
    context = "\n\n".join(content_chunks)
    prompt = f"""
    You are an expert technical assistant.

    Answer clearly using ONLY the context below.

    If the answer is not in the context, say:
    "I don't have enough information in the document."

    Context:
    {context}

    Question:
    {question}

    Answer:
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user", "content":prompt}],
        max_tokens=300
    )

    print('response from OpenAI: {}'.format(response))
    return response.choices[0].message.content


