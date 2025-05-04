import torch
from transformers import pipeline

model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"


def resume_text(original_text: str) -> str:
    pipe = pipeline(
        "text-generation",
        model=model_name,
        torch_dtype=torch.bfloat16,
        device_map="auto",  # Use available GPU if present
    )

    messages = [
        {
            "role": "system",
            "content": (
                "Você é um assistente especializado em redação e síntese de textos longos. "
                "Seu objetivo é transformar textos extensos em resumos curtos, preservando o máximo de detalhes e informações relevantes. "
                "Instruções: "
                "- O resumo deve ser escrito em português brasileiro (pt-br). "
                "- Use uma linguagem clara, objetiva e com tom neutro. "
                "- O resumo deve ter no máximo 4 parágrafos e não ultrapassar 500 caracteres no total. "
                "- Antes de escrever o resumo, leia o texto original e entenda o seu conteúdo, calcule o texto para que o resumo seja o mais preciso possível e nao exceda o limite de caracteres."
            ),
        },
        {
            "role": "user",
            "content": (
                original_text
                if isinstance(original_text, str)
                else "\n".join(original_text)
            ),
        },
    ]

    prompt = pipe.tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )

    outputs = pipe(
        prompt,
        max_new_tokens=300,  # Aumentado para garantir respostas completas
        do_sample=True,
        temperature=0.5,  # Reduzido para respostas mais focadas
        top_k=40,  # Ajustado para melhor equilíbrio
        top_p=0.9,  # Ajustado para melhor coerência
        repetition_penalty=1.2,  # Adicionado para evitar repetições
        num_return_sequences=1,  # Garantir uma única resposta
        pad_token_id=pipe.tokenizer.eos_token_id,  # Configuração adequada de padding
    )

    generated_text = outputs[0]["generated_text"]

    # Extrair apenas a resposta do assistente, removendo o prompt
    assistant_response = generated_text.split("<assistant>")[-1].strip()

    return generated_text
