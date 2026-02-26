from openai import OpenAI
import os

# client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

def generate_answer(question, content_chunks):
    print('come later')
#     context = "\n\n".join(content_chunks)
#     prompt = f"""
#     You mus answer ONLY using the context below.
#     If answer is not found, say you dont know.
#
#     Context: {context}
#     Question: {question}
#
# """
#     response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[{"role":"user", "content":prompt}],
#         max_tokens=300
#     )
#
#     print('response from OpenAI: {}'.format(response))
#     return response.choices[0].message.content


