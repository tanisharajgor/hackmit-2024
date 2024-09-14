import pandas as pd
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M", use_auth_token=True)
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M", use_auth_token=True)

# Check if a GPU is available and move the model to the GPU
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)

# Load language codes
df = pd.read_csv('language-codes.csv')

def translate(source_text, target_language):
    # Get the target language code
    target_lang_code = get_language_code(target_language)
    if target_lang_code is None:
        return "Language code not found."

    # Prepare the input text
    inputs = tokenizer(source_text, return_tensors="pt").to(device)

    # Generate the translation
    translated_tokens = model.generate(
        **inputs, forced_bos_token_id=tokenizer.convert_tokens_to_ids(target_lang_code), max_length=30
    )

    # Decode and return the translated text
    translation = tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]
    return translation

# Define a function to get the code for a given language
def get_language_code(language):
    # Query the DataFrame to find the code for the specified language
    result = df[df['Language'] == language]
    if not result.empty:
        return result['FLORES-200 code'].values[0]
    else:
        return None  # or handle the case where the language is not found

def main():
    print(translate("bottle", "Spanish"))

# Ensure the main function is called
if __name__ == "__main__":
    main()
