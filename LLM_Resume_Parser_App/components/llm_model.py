from langchain_groq import ChatGroq

llm = ChatGroq(temperature=0, model_name="llama3-8b-8192",groq_api_key="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",
 model_kwargs={"response_format": {"type": "json_object"}})

