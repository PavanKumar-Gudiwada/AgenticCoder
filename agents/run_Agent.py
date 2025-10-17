from agents.graph import create_graph, GraphState


def run_agentic_pipeline(prompt: str):
    # Initialize the state schema
    state = GraphState(
        user_prompt=prompt,
        iteration=0,
        plan={},
        code_output={},
        test_output={},
        feedback="",
        error="",
    )

    # Build the graph
    graph = create_graph(state)

    print("\n🚀 Starting LangGraph Agentic Coding Pair\n")
    # Run the graph
    final_state = graph.invoke(state)
    print("\n🏁 Agent completed!")

    return final_state


if __name__ == "__main__":
    user_prompt = input("Describe your coding project idea: ").strip()
    run_agentic_pipeline(user_prompt)
