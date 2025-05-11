import os

import dotenv
from langchain_groq import ChatGroq

dotenv.load_dotenv(".env")

if "GROQ_API_KEY" not in os.environ:
    assert "MISSING API KEYS"


def main():
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
    )

    res = llm.invoke(input="hello")
    print(res)


if __name__ == "__main__":
    main()
