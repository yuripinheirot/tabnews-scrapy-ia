import torch
from transformers import pipeline

model_name = "facebook/bart-large-cnn"


def summarization_ai(original_text: str) -> str:
    pipe = pipeline(
        "summarization",
        model=model_name,
        device_map="cpu",  # Use available GPU if present
    )

    # Configurações para o resumo
    outputs = pipe(
        original_text,
        max_length=2000,  # Limita o tamanho do resumo
        min_length=30,  # Garante um resumo com tamanho mínimo
        do_sample=False,  # Desativa amostragem para resultados determinísticos
        truncation=True,  # Trunca textos muito longos
    )

    # Extrai o texto resumido
    summary = outputs[0]["summary_text"]

    return summary
