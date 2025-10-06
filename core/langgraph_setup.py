

from langgraph import Graph, Node
from agents.idea_collector import IdeaCollectorAgent
from agents.similarity_agent import SimilarityAgent
from agents.critique_agent import CritiqueAgent
from agents.advisor_agent import AdvisorAgent

# Each agent is represented as a LangGraph Node.

class LangGraphSetup:
    def __init__(self):
        self.graph = Graph()
        self.collector = IdeaCollectorAgent()
        self.similarity = SimilarityAgent()
        self.critique = CritiqueAgent()
        self.advisor = AdvisorAgent()
        self._build_graph()

    def _build_graph(self):
        """
        Build the multi-agent flow:
        1. Collector gathers user input.
        2. Similarity Agent checks for matching ideas.
        3. Branch:
           - If similar idea found → AdvisorAgent
           - If not similar → CritiqueAgent
        """

        # Define nodes for agents
        n_collector = Node(id="idea_collector", func=self.collector.collect_idea)
        n_similarity = Node(id="similarity_agent", func=self.similarity.check)
        n_critique = Node(id="critique_agent", func=self.critique.provide_feedback)
        n_advisor = Node(id="advisor_agent", func=self.advisor.present_similar_idea)

        # Add nodes to graph
        self.graph.add_nodes([n_collector, n_similarity, n_critique, n_advisor])

        # Define edges / transitions
        self.graph.add_edge("idea_collector", "similarity_agent")
        self.graph.add_conditional_edges(
            "similarity_agent",
            condition=lambda output: "similar" if output[0] else "new",
            conditional_map={
                "similar": "advisor_agent",
                "new": "critique_agent"
            }
        )

    def execute(self, user_inputs):
        """Execute graph from idea collection to final response."""
        return self.graph.run(start_node="idea_collector", input_data=user_inputs)

# Example Usage:
# from core.langgraph_setup import LangGraphSetup
# orchestrator = LangGraphSetup()
# response = orchestrator.execute(user_inputs)
# print(response)
