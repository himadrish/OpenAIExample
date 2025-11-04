from trulens_eval import Tru, Feedback
from trulens_eval.tru_chain import TruChain
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# Build your chain
llm = OpenAI(model="gpt-4")
prompt = PromptTemplate(template="Summarize: {text}", input_variables=["text"])
chain = LLMChain(llm=llm, prompt=prompt)

# Wrap with TruLens
tru_chain = TruChain(chain, app_id="summary_app")

# Define feedback (helpfulness)
f_helpful = Feedback(
    name="helpfulness",
    criteria="Was this summary accurate and useful?"
)

# Run and evaluate
tru_chain.evaluate(inputs={"text": "AI is transforming the tech industry."}, feedbacks=[f_helpful])
