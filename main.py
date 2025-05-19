import chainlit as cl
from my_secrets import Secrets
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_default_openai_client, set_tracing_disabled
from typing import cast
import json

@cl.on_chat_start
async def start():
    secrets = Secrets()
    provider = AsyncOpenAI(
        api_key=secrets.gemini_api_key,
        base_url=secrets.gemini_base_url
    )
    set_tracing_disabled(True)
    set_default_openai_client(provider)
    agent = Agent(
        name="Assistant",
        instructions="Helpful in problem solving",
        model = OpenAIChatCompletionsModel(
            model=secrets.gemini_api_model,
            openai_client = provider
        )
    )
    cl.user_session.set("agent",agent)
    cl.user_session.set("history",[])
    await cl.Message(
        content="ChainLit ChatBot",
    ).send()

@cl.on_message
async def main(msg: cl.Message):
    agent : Agent = cast(Agent,cl.user_session.get("agent"))
    history:list = cl.user_session.get("history") or []
    
    history.append({
        "role":"user",
        "content":msg.content,
    })

    result = Runner.run_sync(
        starting_agent=agent,
        input=history
    )
    
    history.append({
        "role":"assistant",
        "content":result.final_output
    })

    cl.user_session.set("history",history)
    msg = cl.Message(
        content =result.final_output
    )
    await msg.send()

@cl.on_chat_end
async def end():
    history = cl.user_session.get("history") or []

    with open("chat_history.json","w") as f:
        json.dump(history,f,indent= 4)

