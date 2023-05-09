import pandas as pd
from tqdm import tqdm
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    Trainer,
    TrainingArguments,
)
from transformers.tokenization_utils_base import BatchEncoding


class SimpleDataset:
    def __init__(self, tokenized_texts):
        self.tokenized_texts = tokenized_texts

    def __len__(self):
        return len(self.tokenized_texts["input_ids"])

    def __getitem__(self, idx):
        return {k: v[idx] for k, v in self.tokenized_texts.items()}


def get_average_prediction_label(predictions) -> str:
    means = predictions.predictions.mean(axis=0)

    if means[0] > means[1]:
        label = "NEGATIVE"

    else:
        label = "POSITIVE"

    return label


# Importing data
data = pd.read_csv("matched_speeches_only.csv", keep_default_na=False)
print(data.shape)

# Loading into corpus
corpus = data["text"].values.tolist()  # type: ignore

pretrained_model = "siebert/sentiment-roberta-large-english"
model = AutoModelForSequenceClassification.from_pretrained(pretrained_model)

# Required to prevent a tqdm progress bar
trainer_args = TrainingArguments(disable_tqdm=True, output_dir="tmp_trainer")
trainer = Trainer(model=model, args=trainer_args)
tokenizer = AutoTokenizer.from_pretrained(pretrained_model)


def process_article_text(text) -> str:
    tokenized_text = tokenizer([text], truncation=False, padding=False)
    pred_dataset = SimpleDataset(tokenized_text)

    raw_tokens = pred_dataset[0]["input_ids"]
    token_length = len(raw_tokens)

    if token_length > 512:
        # How many 'chunks' of 512 fit into the total length
        int_quotient = token_length // 512

        # Find the index / interval for where to cut the chunks
        split_index = token_length // (int_quotient + 1)
        token_batches = [
            raw_tokens[i * split_index : (i + 1) * split_index]
            for i in range(int_quotient + 1)
        ]

        # Rebuild the prediction dataset for each chunk
        batch_dict = {
            "input_ids": token_batches,
            "attention_mask": [[1] * len(token_batch) for token_batch in token_batches],
        }
        tokenized_text = BatchEncoding(data=batch_dict)
        pred_dataset = SimpleDataset(tokenized_text)

    predictions = trainer.predict(pred_dataset)
    return get_average_prediction_label(predictions)


data["label"] = [process_article_text(article) for article in tqdm(corpus)]
print(data.head())

data.to_csv("debates_sentiments_NEW.csv", index=False)