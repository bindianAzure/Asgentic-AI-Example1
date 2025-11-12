# Asgentic-AI-Example1

Step 1 - Create virtual environment at python terminal using below command
          py -m venv project1

Step 2 - Activate your virtual environment using below command  
          project1\scripts\activate

Step 3 - Install dependent libraries 
          pip install langchain langchain-openai langchain-community python-dotenv

Step 4 - Either map or create main.py file like this repository 

Step 5 - Run by below command 
          py main.py

🧩 What’s happening

🧠 The agent thinks via decide_tool() whether to use a tool or just respond.
⚙️ Uses the RunnableGraph system (RunnableMap, RunnableLambda, RunnableBranch) to define a decision → action → output flow.
🪄 calculator acts as a “tool” function the agent can invoke dynamically.

Output Example
💡 Final Answer: 722.5
         
