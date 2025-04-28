import pandas as pd
import torch
from sklearn.model_selection import train_test_split
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from datasets import Dataset, Value

# 1. Датасетті оқу
df = pd.read_csv('data/dataset_fixed.csv')

# 📢 Колонка аттарын дұрыстаймыз
df.columns = ['text', 'label']

# 🛠 Тексеру үшін принт қоямыз
print(df.head())
print(df.columns)

# 2. Лейблдарды цифрға ауыстыру
label2id = {
    'Экстремизм жоқ': 0,
    'Политический экстремизм': 1,
    'Ксенофобия': 2,
    'Религиозный экстремизм': 3,
}
id2label = {v: k for k, v in label2id.items()}

df['label'] = df['label'].map(label2id)

# 3. Тек дұрыс жазылған мәліметтерді қалдыру
df = df.dropna(subset=['text', 'label'])
df = df[df['label'].isin([0, 1, 2, 3])]
df = df.reset_index(drop=True)

# 4. Train/Test бөлу
train_texts, val_texts, train_labels, val_labels = train_test_split(
    df['text'].tolist(),
    df['label'].tolist(),
    test_size=0.2,
    random_state=42
)

# 5. Токенизация
tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')

train_encodings = tokenizer(train_texts, truncation=True, padding=True, max_length=512)
val_encodings = tokenizer(val_texts, truncation=True, padding=True, max_length=512)

# 6. Датасеттер жасау
train_dataset = Dataset.from_dict({
    'input_ids': train_encodings['input_ids'],
    'attention_mask': train_encodings['attention_mask'],
    'labels': train_labels
})
val_dataset = Dataset.from_dict({
    'input_ids': val_encodings['input_ids'],
    'attention_mask': val_encodings['attention_mask'],
    'labels': val_labels
})

train_dataset = train_dataset.cast_column('labels', Value('int64'))
val_dataset = val_dataset.cast_column('labels', Value('int64'))

# 7. Модельді жүктеу
model = BertForSequenceClassification.from_pretrained(
    'bert-base-multilingual-cased',
    num_labels=4,
    id2label=id2label,
    label2id=label2id
)

# 8. Тренинг аргументтер
training_args = TrainingArguments(
    output_dir='./models/saved_model/',
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=4,
    logging_dir='./logs',
    save_total_limit=1,
    save_strategy="epoch"
)


# 9. Тренер жасау
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
)

# 10. Fine-tune бастау
trainer.train()

# 11. Модельді сақтау
model.save_pretrained('models/saved_model/')
tokenizer.save_pretrained('models/saved_model/')

print("✅ Fine-tune сәтті аяқталды және модель сақталды!")
