from openai import OpenAI
client = OpenAI()

client.fine_tuning.jobs.create(
  training_file="file-K0KnYE8GRywptqF8MTZmFrRO", 
  model="ft:gpt-4o-mini-2024-07-18:ipt::AB5yM1pa:ckpt-step-84"
)