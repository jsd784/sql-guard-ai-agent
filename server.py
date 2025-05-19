# server.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langserve import add_routes
from langchain_core.runnables import RunnableLambda

from sql_guard_runnable import sql_guard_function

app = FastAPI(
    title="SQL Guard Agent",
    version="1.0",
    description="An agent that classifies SQL queries by risk and optionally executes them."
)

# Enable CORS if calling from a frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Register the agent
add_routes(
    app,
    RunnableLambda(sql_guard_function),
    path="/sql-guard"
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
