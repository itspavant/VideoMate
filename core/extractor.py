import os
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama

def get_llm():
    provider = os.getenv("LLM_PROVIDER", "groq").lower()

    if provider == "ollama":
        return ChatOllama(
            model=os.getenv("OLLAMA_MODEL", "llama3.2:3b"),
            temperature=0,
        )

    return ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0,
    )


def build_chain(system_prompt_text : str):
    llm = get_llm()

    system_prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt_text),
        ("human", "{text}")
    ])

    return (system_prompt | llm | StrOutputParser())


def split_transcript(transcript: str) -> list:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=3000,
        chunk_overlap=200
    )

    return splitter.split_text(transcript)

def extract_with_map_reduce( transcript: str,
    map_prompt: str,
    reduce_prompt: str
) -> str:

    chunks = split_transcript(transcript)

    map_chain = build_chain(map_prompt)

    partial_results = [
        map_chain.invoke({"text": chunk})
        for chunk in chunks
    ]

    combined = "\n\n".join(partial_results)

    reduce_chain = build_chain(reduce_prompt)

    return reduce_chain.invoke({"text": combined})

def extract_action_items(transcript: str) -> str:

    return extract_with_map_reduce(
        transcript,

        "You are an expert meeting analyst. From the meeting transcript, "
        "extract all action items. For each provide:\n"
        "- Task description\n"
        "- Owner (who is responsible)\n"
        "- Deadline (if mentioned, else write 'Not specified')\n\n"
        "Format as a numbered list. If none found say 'No action items found.'",

        "You are an expert meeting analyst. Merge the extracted action items, "
        "remove duplicates, keep the most complete information and return the "
        "same numbered list format. If none exist, return 'No action items found.'"
    )


def extract_key_decisions(transcript: str) -> str:

    return extract_with_map_reduce(
        transcript,

        "You are an expert meeting analyst. From the meeting transcript, "
        "extract all key decisions made. Format as a numbered list. "
        "If none found say 'No key decisions found.'",

        "Merge all extracted key decisions, remove duplicates and return the "
        "same numbered list format. If none exist, return "
        "'No key decisions found.'"
    )


def extract_questions(transcript: str) -> str:

    return extract_with_map_reduce(
        transcript,

        "From the meeting transcript, extract all unresolved questions "
        "or topics needing follow-up. Format as a numbered list. "
        "If none found say 'No open questions found.'",

        "Merge all unresolved questions, remove duplicates and return the "
        "same numbered list format. If none exist, return "
        "'No open questions found.'"
    )
