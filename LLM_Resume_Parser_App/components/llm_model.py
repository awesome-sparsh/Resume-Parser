from langchain_groq import ChatGroq

llm = ChatGroq(temperature=0, model_name="llama3-8b-8192",groq_api_key="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",
 model_kwargs={"response_format": {"type": "json_object"}})

