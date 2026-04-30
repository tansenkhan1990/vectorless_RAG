from openai import OpenAI
from app.config.settings import settings

# Initialize the OpenAI client for agent functionality
client = OpenAI(
    api_key=settings.API_KEY,
    base_url=settings.BASE_URL
)

# Initialize the PDF Knowledge Agent using raw OpenAI client
# This agent is configured to answer questions based only on provided PDF content
def answer_question(prompt: str) -> str:
    """
    Generate an answer using OpenAI API based on the provided prompt.
    
    Args:
        prompt (str): The formatted prompt with context and question
    
    Returns:
        str: The generated answer
    """
    response = client.chat.completions.create(
        model=settings.MODEL,
        messages=[
            {
                "role": "system",
                "content": "Answer only from provided PDF content. Never hallucinate. If the answer is not found in the provided context, say \"I don't know.\" Be precise and cite specific information from the documents."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
        max_tokens=1000
    )
    
    return response.choices[0].message.content