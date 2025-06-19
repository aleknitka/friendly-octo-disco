# Friendly Octo Disco

This repository contains small experiments. The `refine_app.py` script demonstrates how to use [CrewAI](https://crewai.com) together with a simple Gradio interface.

Run the application with LM Studio running locally:

```bash
python refine_app.py
```

Ensure LM Studio's API server is enabled and matches the endpoint and model defined in `constants.py`. The interface will first generate clarifying questions for your initial query. After you provide answers, it produces a refined query.
