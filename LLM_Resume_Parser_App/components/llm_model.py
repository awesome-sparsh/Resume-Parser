from langchain_groq import ChatGroq

llm = ChatGroq(temperature=0, model_name="llama3-8b-8192",groq_api_key="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",
 model_kwargs={"response_format": {"type": "json_object"}})

