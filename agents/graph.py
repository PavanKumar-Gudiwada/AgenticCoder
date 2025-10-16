from langgraph.graph import StateGraph, END
from typing import TypedDict
from agents.planner_agent import PlannerAgent
from agents.coder_agent import CoderAgent
from agents.tester_agent import TesterAgent


# -----------------------------
# Define State Schema using TypedDict
# -----------------------------
class GraphState(TypedDict):
    user_prompt: str
    iteration: int
    plan: dict
    code_output: dict
    test_output: dict
    feedback: str
    error: str


# -----------------------------
# Initialize Agents
# -----------------------------
planner = PlannerAgent()
coder = CoderAgent()
tester = TesterAgent()


# -----------------------------
# Planner Node
# -----------------------------
def plan_node(state: GraphState) -> GraphState:
    prompt = state.get("user_prompt")
    feedback = state.get("feedback")
    current_plan = state.get("plan")

    if not prompt:
        raise ValueError("No user_prompt found in state")

    if feedback and current_plan:
        print("\n🔄 [Planner] Revising plan based on feedback...")
        # Assume planner.plan_project can handle revision logic if a plan is provided
        plan = planner.plan_project(prompt, plan=current_plan, feedback=feedback)
    else:
        print("\n📋 [Planner] Generating initial plan...")
        plan = planner.plan_project(prompt)

    if not plan or "modules" not in plan:
        print("❌ [Planner] Failed to generate a valid plan.")
        state["error"] = "Invalid plan"
        return state

    state["plan"] = plan
    print("✅ [Planner] Plan ready with", len(plan["modules"]), "modules.")
    return state


# -----------------------------
# Coder Node
# -----------------------------
def code_node(state: GraphState) -> GraphState:
    plan = state.get("plan")
    feedback = state.get("feedback")  # Crucial: Get feedback for revision

    if not plan:
        raise ValueError("Missing plan in state")

    # CRITICAL FIX: Use the new single function name
    state["code_output"] = coder.generate_or_improve_code(plan, feedback)
    return state


# -----------------------------
# Tester Node
# -----------------------------
def test_node(state: GraphState) -> GraphState:
    print("\n🧪 [Tester] Running tests...")
    # NOTE: The test execution here is simple; in a real scenario, the code_output would be executed.
    output = tester.run_tests()  # Pass code to tester
    feedback = tester.analyze_results(output)
    state["test_output"] = output
    state["feedback"] = feedback
    print("🔍 [Tester Feedback]:", feedback)
    return state


# -----------------------------
# Decide Next Node (Loop Logic)
# -----------------------------
def decide_next(state: GraphState) -> str:
    iteration = state.get("iteration", 0)
    max_iterations = 3

    if "passed" in state.get("feedback", "").lower():
        print("\n✅ [Graph] Tests passed. Ending pipeline.")
        return END

    if iteration >= max_iterations:
        print(f"⚠️ [Graph] Max retries ({max_iterations}) reached. Ending pipeline.")
        return END

    state["iteration"] = iteration + 1
    # CRITICAL FIX: Send flow back to 'code' to allow for improvements based on feedback
    print(
        f"\n🔁 [Graph] Retry {state['iteration']}/{max_iterations}: → coder → tester loop."
    )
    return "code"


# -----------------------------
# Graph Construction
# -----------------------------
def create_graph(initial_state: GraphState) -> StateGraph:
    # StateGraph needs to be initialized with the state class, not an instance
    graph = StateGraph(GraphState)

    # Add nodes
    graph.add_node("plan", plan_node)
    graph.add_node("code", code_node)
    graph.add_node("test", test_node)

    # Define flow
    graph.set_entry_point("plan")

    # Initial flow
    graph.add_edge("plan", "code")
    graph.add_edge("code", "test")

    # Conditional looping edge: 'test' decides if we loop back to 'plan' or END
    graph.add_conditional_edges(
        "test",
        decide_next,
        {
            "code": "code",  # If we need a retry, go back to code to improve
            END: END,  # If successful or max retries, end
        },
    )

    return graph.compile()
