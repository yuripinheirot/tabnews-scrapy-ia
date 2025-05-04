import torch
from transformers.pipelines import pipeline

pipe = pipeline(
    "text-generation",
    model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    torch_dtype=torch.bfloat16,
    device_map="auto",
)


messages = [
    {
        "role": "user",
        "content": "Quanto é 2 + 2?",
    },
]

prompt = pipe.tokenizer.apply_chat_template(
    messages, tokenize=False, add_generation_prompt=True
)

outputs = pipe(
    prompt, max_new_tokens=256, do_sample=True, temperature=0.7, top_k=50, top_p=0.95
)

print("Resultado: ", outputs)
