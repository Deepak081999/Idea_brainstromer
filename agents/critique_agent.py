from core.llm_client import GeminiLLM


class CritiqueAgent:
    def __init__(self):
        self.llm = GeminiLLM()


    def provide_feedback(self, idea_data):
        prompt = f"""Review the following business idea and suggest improvements:
        Idea: {idea_data['name']}
        Purpose: {idea_data['purpose']}
        Problem: {idea_data['problem']}
        Advantage: {idea_data['advantage']}
        Business Model: {idea_data['business_model']}
        Features: {idea_data['features']}
        Scaling: {idea_data['scaling']}"""
        return self.llm.ask(prompt)