# Friendly Octo Disco

This repository contains small experiments. The `refine_app.py` script demonstrates how to use [CrewAI](https://crewai.com) together with a chat-style Gradio interface.

Run the application with:

```bash
python refine_app.py
```

The interface will first generate clarifying questions for your initial query. After you provide answers, it produces a refined query.

Agent roles and tasks are defined in YAML files inside the `agents/` directory so they can be tweaked without modifying code.
