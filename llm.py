from langchain import HuggingFaceHub, PromptTemplate, LLMChain


class Assistant():
    def __init__(self):
        huggingfacehub_api_token = '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'

        repo_id = "tiiuae/falcon-7b-instruct"
        self.llm = HuggingFaceHub(huggingfacehub_api_token=huggingfacehub_api_token,
                                  repo_id=repo_id,
                                  model_kwargs={"temperature": 0.6, "max_new_tokens": 2000})

        self.template = """
        Extract the question, addressed to Misha based on the context below. Respond with the question Misha was asked.

        context: {context}

        """

        self.prompt = PromptTemplate(template=self.template, input_variables=["context"])
        self.llm_chain = LLMChain(prompt=self.prompt, llm=self.llm, verbose=True)

    def detect_question(self, context):
        resp = self.llm_chain.run(
            context=context)
        print(resp)

# question = "How to cook pasta?"
#
# print(llm_chain.run(question))


# @cl.langchain_factory
# def factory():
#     prompt = PromptTemplate(template=template, input_variables=["question"])
#     llm_chain = LLMChain(prompt=prompt, llm=llm, verbose=True, streaming=True)
#
#     return llm_chain

# @cl.on_chat_start
# async def main():
#     # Instantiate the chain for that user session
#     prompt = PromptTemplate(template=template, input_variables=["question"])
#     llm_chain = LLMChain(prompt=prompt, llm=llm, verbose=True)
#
#     # Store the chain in the user session
#     cl.user_session.set("llm_chain", llm_chain)
#     await asyncio.sleep(10)
#     resp = llm_chain.run(question="Misha, how are you doing today?")
#     await cl.write(resp)
#
#
# @cl.on_message
# async def main(message: str):
#     # Retrieve the chain from the user session
#     llm_chain = cl.user_session.get("llm_chain")  # type: LLMChain
#
#     # Call the chain asynchronously
#     res = await llm_chain.acall(message, callbacks=[cl.AsyncLangchainCallbackHandler()])
#
#     # Do any post processing here
#
#     # Send the response
#     await cl.Message(content=res["text"]).send()
#
