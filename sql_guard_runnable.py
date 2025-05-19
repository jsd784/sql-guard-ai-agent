# sql_guard_runnable.py

import os
import json
import logging
from typing import Any, Dict

from pydantic import BaseModel, Field, SecretStr
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain_openai import AzureChatOpenAI

from db.crud import is_ip_banned, create_access_log, get_data_in_json

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Input model
class SQLGuardInput(BaseModel):
    sql_query: str
    ip_address: str

# Output model
class SQLGuardOutput(BaseModel):
    status: str
    risk: str = ""
    reason: str = ""
    query_result: Any = None
    error: str = ""

# LLM and prompt
llm = AzureChatOpenAI(
    api_key=SecretStr(os.getenv("AZURE_OPENAI_API_KEY")),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    model="gpt-4o",
    openai_api_type="azure_openai",
    api_version="2024-08-01-preview",
    temperature=0
)

class RiskAssessment(BaseModel):
    risk: str = Field(..., description="Risk level: high, medium, or low")
    reason: str = Field(..., description="Short reason for the assigned risk level")

parser = PydanticOutputParser(pydantic_object=RiskAssessment)

prompt = ChatPromptTemplate.from_messages([
    ("system", (
        "You are a database security expert. Analyze the following SQL query for risks "
        "like injection, admin access, or sensitive data leaks. Respond using only the JSON schema provided.\n\n"
        "{format_instructions}"
    )),
    ("human", "{sql_query}")
])

# This is the function LangServe will expose
def sql_guard_function(input: Dict[str, Any]) -> dict[str, Any]:
    try:
        data = SQLGuardInput(**input)
        sql_query = data.sql_query
        ip = data.ip_address

        if is_ip_banned(ip):
            return SQLGuardOutput(
                status="failed", risk="high", reason="IP is banned", error="Access Denied"
            ).dict()

        formatted = prompt.format_messages(
            sql_query=f"```sql\n{sql_query}\n```",
            format_instructions=parser.get_format_instructions()
        )

        response = llm.invoke(formatted)
        parsed = parser.parse(response.content)

        banned = parsed.risk.lower() == "high"
        create_access_log(ip=ip, sql=sql_query, risk=parsed.risk, banned=banned)

        if banned:
            return SQLGuardOutput(
                status="failed", risk=parsed.risk, reason=parsed.reason, error="High risk detected"
            ).dict()

        return SQLGuardOutput(
            status="not banned",
            risk=parsed.risk,
            reason=parsed.reason,
            query_result=get_data_in_json(sql_query)
        ).dict()

    except Exception as e:
        logger.exception("Error in sql_guard_function")
        return SQLGuardOutput(status="failed", error=str(e)).dict()
