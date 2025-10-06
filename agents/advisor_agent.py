from core.llm_client import GeminiLLM

class AdvisorAgent:
    def __init__(self):
        self.llm = GeminiLLM()

    def chat_with_existing_idea(self, matched_idea, user_question):
        """
        Allows user to ask questions about the existing idea.
        The matched_idea dict provides context.
        """
        context = f"""
You are helping the user understand this existing idea:
Name: {matched_idea['name']}
Purpose: {matched_idea['purpose']}
Problem: {matched_idea['problem']}
Advantage: {matched_idea['advantage']}
Business Model: {matched_idea['business_model']}
Features: {matched_idea['features']}
Scaling: {matched_idea['scaling']}
"""
        prompt = context + f"\nUser Question: {user_question}\nAnswer:"
        return self.llm.ask(prompt)

    def present_similar_idea(self, matched_idea, score):
        # Return message + instruction for chat
        message = (
            f"We found a similar idea ({score}% match):\n"
            f"Name: {matched_idea['name']}\nPurpose: {matched_idea['purpose']}\n"
            f"Problem: {matched_idea['problem']}\n"
            "You can now ask questions about this idea and explore it interactively."
        )
        return message, matched_idea  # return matched_idea for chat usage
