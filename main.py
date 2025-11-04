from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


# Initialize OpenAI client (make sure OPENAI_API_KEY is set in your environment)
client = OpenAI()

def healthcare_chatbot(user_input):
    """
    A simple AI-powered healthcare assistant.
    It provides general health, fitness, nutrition, and symptom information.
    Not a substitute for professional medical advice.
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful and knowledgeable virtual healthcare assistant. "
                    "You can answer general health, wellness, and fitness questions, "
                    "provide education on common symptoms, and recommend when a user should see a doctor. "
                    "You are not a doctor and should not diagnose or prescribe medicine. "
                    "Always include a disclaimer reminding users to consult a licensed healthcare provider."
                )
            },
            {"role": "user", "content": user_input}
        ],
        temperature=0.7,
    )

    # Extract the text safely from the response
    return response.choices[0].message.content[0]["text"]

# Example interaction
if __name__ == "__main__":
    print("🤖 HealthBot: Hello! I can help you with health and wellness information.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("🤖 HealthBot: Take care and stay healthy!")
            break
        answer = healthcare_chatbot(user_input)
        print(f"🤖 HealthBot: {answer}")

