import torch
from transformers import pipeline, AutoTokenizer

model_name = "facebook/bart-large-cnn"


def summarization_ai(original_text: str) -> str:
    tokenizer = AutoTokenizer.from_pretrained(model_name, model_max_length=1024)

    pipe = pipeline(
        "summarization",
        model=model_name,
        tokenizer=tokenizer,
        device_map="cpu",
    )

    outputs = pipe(
        original_text,
        max_length=1024,  # Limita o tamanho do resumo
        min_length=128,  # Garante um resumo com tamanho mínimo
        do_sample=False,  # Desativa amostragem para resultados determinísticos
        truncation=True,  # Trunca textos muito longos
        num_workers=4,  # Aumenta o número de threads para processamento
    )

    summary = outputs[0]["summary_text"]

    return summary
