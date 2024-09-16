from nodes import Nodes
from state import LottoState
from langgraph.graph import StateGraph, END, MessagesState
from langchain_core.messages import HumanMessage

class Workflow():
    def __init__(self):
        nodes = Nodes()
        supervisor = nodes.supervisor()
        lotto_node = nodes.lotto_node()
        coder_node = nodes.coder_node()
        workflow = StateGraph(LottoState)
        workflow.add_node("Lotto_Manager", lotto_node)
        workflow.add_node("Coder", coder_node)
        workflow.add_node("supervisor", supervisor)
    
        members = ["Lotto_Manager", "Coder"]    
        for member in members:
    # We want our workers to ALWAYS "report back" to the supervisor when done
            workflow.add_edge(member, "supervisor") # add one edge for each of the agents
        # The supervisor populates the "next" field in the graph state
        # which routes to a node or finishes
        conditional_map = {k: k for k in members}
        conditional_map["FINISH"] = END
        workflow.add_conditional_edges("supervisor", lambda x: x["next"], conditional_map)
        # Finally, add entrypoint
        workflow.set_entry_point("supervisor")

        self.app = workflow.compile()
    
    def response(self, query:str):
        return self.app.invoke(input=
        {
        "messages": [
            HumanMessage(content=query)]}, 
            #debug=True
            )