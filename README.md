# Friendly Octo Disco

This repository contains small experiments. The `refine_app.py` script demonstrates how to use [CrewAI](https://crewai.com) together with a simple Gradio interface.

Run the application with:

```bash
OPENAI_API_KEY=your-key python refine_app.py
```

The interface will first generate clarifying questions for your initial query. After you provide answers, it produces a refined query.
