import operator
from typing import Annotated, TypedDict, Union
from langchain_ollama import OllamaLLM
from langgraph.graph import StateGraph, END

# 1. Define the State (How the agent remembers what it did)
class AgentState(TypedDict):
    question: str
    plan: str
    steps: Annotated[list, operator.add]
    response: str

# Use the lighter model we pulled earlier
llm = OllamaLLM(model="phi3")

# 2. Define the Nodes (The reasoning steps)
def planner(state: AgentState):
    print("--- NODE: PLANNER ---")
    # Simulating the 'task decomposition' mentioned in your CV
    return {"plan": f"Decomposing task: {state['question']}"}

def executor(state: AgentState):
    print("--- NODE: EXECUTOR ---")
    # Simulating 'tool selection'
    return {"steps": ["Accessed Network DB", "Validated Latency"], 
            "response": "Agent reasoning complete: All nodes optimized."}

# 3. Build the Graph (The 'Agentic Workflow')
workflow = StateGraph(AgentState)

workflow.add_node("planner", planner)
workflow.add_node("executor", executor)

workflow.set_entry_point("planner")
workflow.add_edge("planner", "executor")
workflow.add_edge("executor", END)

# Compile the workflow
app = workflow.compile()

# 4. Test Run
if __name__ == "__main__":
    inputs = {"question": "Optimize traffic for Bhubaneswar 5G Cluster"}
    for output in app.stream(inputs):
        print(output)