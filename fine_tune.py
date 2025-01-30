from transformers import MarianMTModel, MarianTokenizer, Trainer, TrainingArguments, DataCollatorForSeq2Seq
from datasets import load_dataset
import re

dataset = load_dataset("text", data_files={"train": ["tuning-lyricstranslate/source.txt", "tuning-lyricstranslate/target.txt"]})

model_name = "Helsinki-NLP/opus-mt-en-ru"
model = MarianMTModel.from_pretrained(model_name)
tokenizer = MarianTokenizer.from_pretrained(model_name)

def tokenize_data(examples):
    # TODO: don't get crazy))
    half_len = len(examples["text"]) / 2
    source_texts = examples["text"][0:half_len]
    target_texts = examples["text"][half_len:]

    model_inputs = tokenizer(source_texts, truncation=True, padding="max_length", max_length=128)
    labels = tokenizer(target_texts, truncation=True, padding="max_length", max_length=128)
    model_inputs["labels"] = labels["input_ids"]

    return model_inputs

tokenized_dataset = dataset.map(tokenize_data, batched=True)

training_args = TrainingArguments(
    output_dir="./fine_tuned_model",
    per_device_train_batch_size=8,
    save_steps=500,
    num_train_epochs=5,
    evaluation_strategy="steps",
    learning_rate=5e-5,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    tokenizer=tokenizer,
    data_collator=DataCollatorForSeq2Seq(tokenizer, model),
)

trainer.train()
model.save_pretrained("./fine_tuned_model")
tokenizer.save_pretrained("./fine_tuned_model")

print("Fine-tuning complete! Model saved to `./fine_tuned_model`.")
