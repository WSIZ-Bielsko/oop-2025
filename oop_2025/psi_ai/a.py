from openai import OpenAI


def call_sonar_api():

    YOUR_API_KEY = "pplx-(......)"  #insert your perplexity token here... if you have one....

    # Initialize the client
    client = OpenAI(api_key=YOUR_API_KEY, base_url="https://api.perplexity.ai")

    # Define your messages
    messages = [
        {
            "role": "system",
            "content": "You are an artificial intelligence assistant and you need to engage in a helpful, detailed, polite conversation with a user."
        },
        {
            "role": "user",
            "content": "Count to 100, with a comma between each number and no newlines. E.g., 1, 2, 3, ..."
        }
    ]

    """
    messages = [
    {
        "role": "system",
        "content": "Be precise and concise. [Include detailed system instructions here]"
    },
    {
        "role": "user",
        "content": "[Your long initial context here]"
    },
    {
        "role": "assistant",
        "content": "I understand the context provided."
    },
    {
        "role": "user",
        "content": "[Your first actual question]"
    }
]
    """


    # Make a standard completion request
    response = client.chat.completions.create(
        model="sonar",
        messages=messages
    )

    print(response)
    for i in range(10):
        print(i)

    # # Make a streaming completion request
    # response_stream = client.chat.completions.create(
    #     model="sonar",
    #     messages=messages,
    #     stream=True
    # )

    # for response in response_stream:
    #     print(response)

"""
ChatCompletion(id='5d6a7242-0552-403e-bce6-ddbec6a6ad21', 
choices=[
    Choice(finish_reason='stop', index=0, logprobs=None, 
        message=
        ChatCompletionMessage(content='Certainly Here are the numbers from 1 to 100, listed with commas between each number:\n\n1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100.\n\nIf you\'d like to explore counting in a more engaging way, you might enjoy songs like the "Count to 100 Silly Song" by Jack Hartmann, which combines movement and fun while counting[2]. 
            Alternatively, you could practice counting by hundreds with songs like "The Counting by 100s Song" from Scratch Garden[5]. 
            Let me know if you have any other questions or if there\'s anything else I can help you with', 
            refusal=None, role='assistant', audio=None, function_call=None, tool_calls=None),
             delta={'role': 'assistant', 'content': ''})],

created=1739009813, 
model='sonar', 
object='chat.completion', 
service_tier=None, 
system_fingerprint=None, 
usage=CompletionUsage(completion_tokens=411, prompt_tokens=52, total_tokens=463, completion_tokens_details=None, prompt_tokens_details=None), 
citations=['https://www.englishclub.com/kids/numbers-chart.php', 'https://www.youtube.com/watch?v=2QIwkSVOflU', 
'https://www.busuu.com/en/french/numbers', 'https://peps.python.org/pep-0008/', 'https://www.youtube.com/watch?v=l3R6wdHs9n8'])

"""


if __name__ == '__main__':
    call_sonar_api()