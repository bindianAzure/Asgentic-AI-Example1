import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableBranch, RunnableMap, RunnableLambda



# 1️⃣ Define a simple math tool
@tool
def calculator(expression: str) -> str:
    """Safely evaluate a math expression."""
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error: {e}"

# 2️⃣ Initialize the LLM
llm = ChatOpenAI(model="gpt-4o-mini", api_key="your-key", temperature=0)

# 3️⃣ Define the system prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an intelligent AI agent that can use tools when needed."),
    ("human", "{input}")
])

# 4️⃣ Define the decision logic
def decide_tool(inputs):
    question = inputs["input"].lower()
    if any(op in question for op in ["calculate", "price", "discount", "sum", "multiply", "%"]):
        # Extract expression from text if found
        import re
        numbers = re.findall(r"\d+\.?\d*", question)
        if "discount" in question and len(numbers) >= 2:
            price, discount = float(numbers[0]), float(numbers[1])
            return {"tool": "calculator", "expression": f"{price} * (1 - {discount}/100)"}
        return {"tool": "calculator", "expression": numbers}
    return {"tool": "llm"}

# 5️⃣ Define the tool runner
def run_tool(data):
    if data["tool"] == "calculator":
        return calculator.invoke(data["expression"])
    return "I can only handle basic math in this demo."

# 6️⃣ Create the agent pipeline
agent = (
    RunnableMap({"input": lambda x: x["input"]})
    | RunnableLambda(decide_tool)
    | RunnableBranch(
        (lambda d: d["tool"] == "calculator", RunnableLambda(run_tool)),
        RunnableLambda(lambda _: "No tool needed for this query.")
    )
)

# 7️⃣ Run the agent
query = "If a laptop costs 850 dollars and has 15% discount, what is the final price?"
result = agent.invoke({"input": query})

print("\n💡 Final Answer:", result)
