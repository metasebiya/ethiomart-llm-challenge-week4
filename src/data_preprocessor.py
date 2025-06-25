# src/data_preprocessor.py

import pandas as pd
import re
import json
from datetime import datetime

class DataPreprocessor:
    def __init__(self):
        pass

    def normalize_amharic(self, text):
        if not text:
            return ""

        replacements = {
            "፣": ",",
            "።": ".",
            "‘": "'", "’": "'",
            "“": '"', "”": '"',
            "፤": ":",  # sometimes used instead of colon
        }

        for orig, repl in replacements.items():
            text = text.replace(orig, repl)

        normalization_dict = {
            # All 'h' variants to 'ሀ'
            'ሐ': 'ሀ', 'ሑ': 'ሁ', 'ሒ': 'ሂ', 'ሓ': 'ሃ', 'ሔ': 'ሄ', 'ሕ': 'ህ', 'ሖ': 'ሆ',
            'ኀ': 'ሀ', 'ኁ': 'ሁ', 'ኂ': 'ሂ', 'ኃ': 'ሃ', 'ኄ': 'ሄ', 'ኅ': 'ህ', 'ኆ': 'ሆ',
            # All 's' variants to 'ሰ'
            'ሠ': 'ሰ', 'ሡ': 'ሱ', 'ሢ': 'ሲ', 'ሣ': 'ሳ', 'ሤ': 'ሴ', 'ሥ': 'ስ', 'ሦ': 'ሶ',
            # All 'ts' variants to 'ፀ'
            'ጸ': 'ፀ', 'ጹ': 'ፁ', 'ጺ': 'ፂ', 'ጻ': 'ፃ', 'ጼ': 'ፄ', 'ጽ': 'ፅ', 'ጾ': 'ፆ',
            # All 'a' variants to 'አ'
            'ዐ': 'አ', 'ዑ': 'ኡ', 'ዒ': 'ኢ', 'ዓ': 'ኣ', 'ዔ': 'ኤ', 'ዕ': 'እ', 'ዖ': 'ኦ',
            # Standard punctuation
            '―': '-', '–': '-', '—': '-',
            '“': '"', '”': '"',
            '‘': "'", '’': "'",
        }

        for char, replacement in normalization_dict.items():
            text = text.replace(char, replacement)

        return text.strip()

    def tokenize_amharic(self, text):
        return text.split()

    def clean_text(self, text):
        text = re.sub(r'http\S+', '', text)
        text = re.sub(r'[^\w\s]', '', text)
        text = re.sub(r'\d+', '', text)
        return ' '.join(text.split()).lower()

    def extract_metadata(self, row):
        return {
            'channel': row['channel'],
            'message_id': row['message_id'],
            'timestamp': row['timestamp'],  # Fixed from 'Date'
            'media_path': row['media_path']
        }

    def preprocess_data(self, input_file, output_file):
        df = pd.read_csv(input_file)

        # Normalize and strip column names to avoid KeyErrors
        df.columns = df.columns.str.strip()

        # Convert timestamp to datetime
        if 'Date' in df.columns:
            df.rename(columns={'Date': 'timestamp'}, inplace=True)
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        processed_data = []

        for _, row in df.iterrows():
            metadata = self.extract_metadata(row)

            content = row['text']
            if not isinstance(content, str):
                content = ""
            content = self.clean_text(content)
            content = self.normalize_amharic(content)
            tokens = self.tokenize_amharic(content)

            processed_data.append({
                'metadata': metadata,
                'content': content,
                'tokens': tokens
            })

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(processed_data, f, ensure_ascii=False, indent=2, default=str)

        print(f"✅ Preprocessed data saved to {output_file}")

# Run as script
if __name__ == "__main__":
    input_file = '../data/raw/telegram_messages.csv'
    output_file = '../data/processed/preprocessed_data.txt'
    preprocessor = DataPreprocessor()
    preprocessor.preprocess_data(input_file, output_file)
