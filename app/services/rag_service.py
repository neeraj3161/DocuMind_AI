from openai import OpenAI
import os

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

def generate_answer(question, content_chunks):
    context = "\n\n".join(content_chunks)
    prompt = f"""
    You are a technical assistant.

    Use the provided context to answer the question.

    If the answer is clearly supported by the context, answer confidently.
    If the context partially supports the answer, use the available information to respond.

    Only say you don't have enough information if the topic is completely unrelated to the context.

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


