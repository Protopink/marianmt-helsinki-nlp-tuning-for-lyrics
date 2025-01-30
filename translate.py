import os
import hashlib
import json
import torch
from transformers import MarianMTModel, MarianTokenizer
from tqdm import tqdm

TUNING_DIR = "./tuning"
INPUT_DIR = "./input"
OUTPUT_DIR = "./output"
CACHE_FILE = "./cache.json"
MODEL_PATH = "./fine_tuned_model"

def translate_texts(texts, model, tokenizer):
    translated_texts = []

    for text in tqdm(texts, desc="Translating"):
        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        translated_tokens = model.generate(**inputs)
        translated_texts.append(tokenizer.decode(translated_tokens[0], skip_special_tokens=True))

    return translated_texts


def translate_files(model, tokenizer, input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    num_translated = 0

    for file_name in os.listdir(input_dir):
        input_path = os.path.join(input_dir, file_name)
        output_path = os.path.join(output_dir, file_name)

        if not os.path.isfile(input_path):
            continue

        print("Translating `{file_name}` to `{output_path}`...")

        with open(input_path, "r", encoding="utf-8") as f:
            texts = f.readlines()

        translated_texts = translate_texts(texts, model, tokenizer)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(translated_texts))

        num_translated += 1
    
    return num_translated


if __name__ == "__main__":
    tokenizer = MarianTokenizer.from_pretrained(MODEL_PATH)
    model = MarianMTModel.from_pretrained(MODEL_PATH)

    num_translated = translate_files(model, tokenizer, INPUT_DIR, OUTPUT_DIR)

    print("Translation complete! Translated", num_translated, "files")
