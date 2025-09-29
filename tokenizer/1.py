from transformers import GPT2Tokenizer, GPT2LMHeadModel
from peft import PeftModel

# Load the fixed tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("./tokenizer")
print(f"✅ Tokenizer size: {len(tokenizer)}")

# Load model with matching size
model = GPT2LMHeadModel.from_pretrained("gpt2")
model.resize_token_embeddings(len(tokenizer))

# Load your fine-tuned adapter
model = PeftModel.from_pretrained(model, "./sandbox_output/checkpoint-21")
print("🎉 Cybersecurity AI loaded successfully!")

# Quick test
test_text = "<|prompt|> test"
inputs = tokenizer(test_text, return_tensors="pt")
outputs = model.generate(**inputs, max_new_tokens=10)
print(f"Test: {tokenizer.decode(outputs[0])}")