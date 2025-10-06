from core.llm_client import GeminiLLM
from core.utils import save_idea, check_similarity
from agents.similarity_agent import SimilarityAgent
from agents.critique_agent import CritiqueAgent
from agents.advisor_agent import AdvisorAgent


class IdeaCollectorAgent:
    def __init__(self):
        self.llm = GeminiLLM()
        self.similarity_agent = SimilarityAgent()
        self.critique_agent = CritiqueAgent()
        self.advisor_agent = AdvisorAgent()


    def collect_idea(self, user_inputs, user_followup=None):
        idea_data = {
            "name": user_inputs.get("Idea Name"),
            "purpose": user_inputs.get("Purpose"),
            "problem": user_inputs.get("Problem"),
            "advantage": user_inputs.get("Advantage"),
            "business_model": user_inputs.get("Business Model"),
            "features": user_inputs.get("Features"),
            "scaling": user_inputs.get("Scaling"),
        }
        idea_data["description"] = " ".join([str(v) for v in idea_data.values() if v])

        is_similar, matched_idea, score = check_similarity(idea_data)
        if is_similar:
            message, matched = self.advisor_agent.present_similar_idea(matched_idea, score)
            # If user sends follow-up question
            if user_followup:
                chat_response = self.advisor_agent.chat_with_existing_idea(matched, user_followup)
                return chat_response
            return message
        else:
            save_idea(idea_data)
            return self.critique_agent.provide_feedback(idea_data)
