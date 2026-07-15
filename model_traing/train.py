from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    Trainer,
    TrainingArguments,
    DataCollatorForLanguageModeling
)

from datasets import load_dataset

print("Loading tokenizer...")

tokenizer = AutoTokenizer.from_pretrained("distilgpt2")

tokenizer.pad_token = tokenizer.eos_token

print("Loading dataset...")

dataset = load_dataset(
    "text",
    data_files={
        "train": "datasets/processed/hybrid_data.txt"
    }
)

def tokenize_function(examples):

    return tokenizer(
        examples["text"],
        truncation=True,
        padding="max_length",
        max_length=128
    )

tokenized_dataset = dataset.map(
    tokenize_function,
    batched=True
)

print("Loading model...")

model = AutoModelForCausalLM.from_pretrained("distilgpt2")

data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False
)

training_args = TrainingArguments(
    output_dir="./checkpoints",
    num_train_epochs=2,
    per_device_train_batch_size=1,
    logging_steps=10,
    save_steps=500,
     learning_rate=5e-5
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    data_collator=data_collator,
)

print("Starting training...")

trainer.train()

print("Saving model...")

model.save_pretrained("./checkpoints/verilog_model")

tokenizer.save_pretrained("./checkpoints/verilog_model")

print("Training complete!")
