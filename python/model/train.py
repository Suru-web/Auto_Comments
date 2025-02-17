import torch
from transformers import AutoTokenizer, T5ForConditionalGeneration, Trainer, TrainingArguments
from sklearn.model_selection import train_test_split
from dataset_preprocessing import load_and_preprocess_data, CodeCommentDataset

# Main training function
def train_model():
    # Load data
    data = load_and_preprocess_data("/Users/surajmeharwade/Projects/Auto_Comments/data/code-comments.json")
    train_data, val_data = train_test_split(data, test_size=0.2, random_state=42)

    # Initialize model and tokenizer
    model_name = "Salesforce/codet5-small"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name)
    
    use_mps = torch.backends.mps.is_available()
    device = torch.device("mps" if use_mps else "cpu")
    model.to(device)
    
    # Create datasets
    train_dataset = CodeCommentDataset(train_data, tokenizer)
    val_dataset = CodeCommentDataset(val_data, tokenizer)

    # Training arguments
    training_args = TrainingArguments(
        output_dir="/Users/surajmeharwade/Projects/Auto_Comments/model/trained-code-comment-model",
        num_train_epochs=10,
        per_device_train_batch_size=4,
        per_device_eval_batch_size=4,
        warmup_steps=500,
        weight_decay=0.01,
        logging_dir="./logs",
        logging_steps=100,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        fp16=False,  # Enable if using GPU
    )

    # Create trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
    )

    # Start training
    trainer.train()

    # Save model
    model.save_pretrained("./trained-code-comment-model")
    tokenizer.save_pretrained("./trained-code-comment-model")

if __name__ == "__main__":
    train_model()
