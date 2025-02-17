import json
from torch.utils.data import Dataset

# Load and preprocess data
def load_and_preprocess_data(file_path):
    with open(file_path, 'r') as f:
        dataset = json.load(f)
    
    processed = []
    for item in dataset:
        processed.append({
            "input_text": item["code"].strip(),
            "target_text": f"{item['comments'].replace('#', '').strip()}"
        })
    return processed

# Custom Dataset class
class CodeCommentDataset(Dataset):
    def __init__(self, data, tokenizer, max_input_length=256, max_target_length=64):
        self.data = data
        self.tokenizer = tokenizer
        self.max_input_length = max_input_length
        self.max_target_length = max_target_length

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item = self.data[idx]
        
        # Tokenize input
        input_encoding = self.tokenizer(
            item["input_text"],
            max_length=self.max_input_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt"
        )
        
        # Tokenize target
        target_encoding = self.tokenizer(
            text_target=item["target_text"],
            max_length=self.max_target_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt"
        )

        return {
            "input_ids": input_encoding["input_ids"].flatten(),
            "attention_mask": input_encoding["attention_mask"].flatten(),
            "labels": target_encoding["input_ids"].flatten()
        }