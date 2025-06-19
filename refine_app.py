import os
import yaml
import gradio as gr
from crewai import Agent, Task, Crew
from constants import LM_STUDIO_ENDPOINT, LM_STUDIO_MODEL_NAME
import openai

from constants import (
    NUM_TURNS,
    END_MESSAGE,
    LM_STUDIO_ENDPOINT,
    LM_STUDIO_API_KEY,
    LM_STUDIO_MODEL,
)


def _load_yaml(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _create_agent(name: str) -> Agent:
    cfg = _load_yaml(os.path.join("agents", f"{name}.yaml"))
    return Agent(
        role=cfg["role"],
        goal=cfg["goal"],
        backstory=cfg["backstory"],
        llm_config={
            "base_url": LM_STUDIO_ENDPOINT,
            "api_key": LM_STUDIO_API_KEY,
            "model": LM_STUDIO_MODEL,
        },
    )


def _task_details(name: str, **fmt) -> tuple[str, str]:
    cfg = _load_yaml(os.path.join("agents", "tasks", f"{name}.yaml"))
    desc = cfg["description"].format(**fmt)
    return desc, cfg["expected_output"]



def ask_questions(user_query: str) -> str:
    """Generate clarifying questions for the given query using CrewAI."""
    clarifier = _create_agent("clarifier")
    desc, out = _task_details("ask_questions", user_query=user_query)
    question_task = Task(description=desc, expected_output=out, agent=clarifier)
    crew = Crew(agents=[clarifier], tasks=[question_task])
    result = crew.kickoff()
    return str(result)


def refine_query(user_query: str, user_answers: str) -> str:
    """Generate a refined query using the initial query and user answers."""
    refiner = _create_agent("refiner")
    desc, out = _task_details(
        "refine_query", user_query=user_query, user_answers=user_answers
    )
    refine_task = Task(description=desc, expected_output=out, agent=refiner)
    crew = Crew(agents=[refiner], tasks=[refine_task])
    result = crew.kickoff()
    return str(result)


def proceed_to_next_display(refined_query: str) -> None:
    """Placeholder for next display after conversation ends."""
    # This function will be fleshed out in future revisions.
    print("Next display would receive:", refined_query)


def chat(message: str, history: list, state: dict) -> tuple[list, dict]:
    """Handle a single chat interaction."""
    if state is None:
        state = {"turns": 0, "initial_query": ""}

    if state["turns"] == 0:
        state["initial_query"] = message
        response = ask_questions(message)
    else:
        response = refine_query(state["initial_query"], message)

    state["turns"] += 1
    history.append((message, response))

    if state["turns"] >= NUM_TURNS:
        history.append(("", END_MESSAGE))
        proceed_to_next_display(response)

    return history, state


def launch_interface() -> None:
    """Launch the Gradio chat interface for query refinement."""
    with gr.Blocks() as demo:
        gr.Markdown("# Query Refinement with CrewAI")
        chatbot = gr.Chatbot()
        msg = gr.Textbox(label="Message")
        state = gr.State({"turns": 0, "initial_query": ""})

        def _submit(user_msg, chat_history, chat_state):
            return chat(user_msg, chat_history, chat_state)

        msg.submit(_submit, inputs=[msg, chatbot, state], outputs=[chatbot, state])
        msg.submit(lambda: "", None, msg)  # clear input

    demo.launch()


if __name__ == "__main__":
    launch_interface()
