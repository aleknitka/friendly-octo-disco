import os
import gradio as gr
from crewai import Agent, Task, Crew

# Ensure API key is provided for the language model
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise EnvironmentError("OPENAI_API_KEY environment variable is required")


def ask_questions(user_query: str) -> str:
    """Generate clarifying questions for the given query using CrewAI."""
    clarifier = Agent(
        role="Clarifier",
        goal="Ask clarifying questions to refine user requests",
        backstory="Expert at gathering specific information.",
    )
    question_task = Task(
        description=(
            f"Provide concise clarifying questions to better understand: {user_query}"
        ),
        expected_output="A numbered list of questions",
        agent=clarifier,
    )
    crew = Crew(agents=[clarifier], tasks=[question_task])
    result = crew.kickoff()
    return str(result)


def refine_query(user_query: str, user_answers: str) -> str:
    """Generate a refined query using the initial query and user answers."""
    refiner = Agent(
        role="Refiner",
        goal="Create a concise refined query",
        backstory="Skilled at summarizing detailed requirements.",
    )
    refine_task = Task(
        description=(
            "Using the initial query and clarifications, produce a single refined "
            f"query.\nInitial query: {user_query}\nClarifications: {user_answers}"
        ),
        expected_output="The refined query",
        agent=refiner,
    )
    crew = Crew(agents=[refiner], tasks=[refine_task])
    result = crew.kickoff()
    return str(result)


def launch_interface() -> None:
    """Launch the Gradio interface for query refinement."""
    with gr.Blocks() as demo:
        gr.Markdown("# Query Refinement with CrewAI")
        query = gr.Textbox(label="Initial query")
        ask_btn = gr.Button("Generate clarifying questions")
        questions = gr.Textbox(label="Questions")
        answers = gr.Textbox(label="Your answers")
        refine_btn = gr.Button("Refine query")
        refined = gr.Textbox(label="Refined query")

        ask_btn.click(ask_questions, inputs=query, outputs=questions)
        refine_btn.click(refine_query, inputs=[query, answers], outputs=refined)

    demo.launch()


if __name__ == "__main__":
    launch_interface()
