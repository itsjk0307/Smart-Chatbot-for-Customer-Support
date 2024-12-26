from transformers import AutoModelForCausalLM, AutoTokenizer

# Load a pre-trained model (e.g., DialoGPT)
model_name = "microsoft/DialoGPT-medium"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

def generate_bot_response(user_message: str) -> str:
    """Generate a chatbot response using a pre-trained AI model."""
    try:
        # Tokenize input and generate response
        input_ids = tokenizer.encode(user_message + tokenizer.eos_token, return_tensors="pt")
        response_ids = model.generate(input_ids, max_length=50, pad_token_id=tokenizer.eos_token_id)
        response = tokenizer.decode(response_ids[:, input_ids.shape[-1]:][0], skip_special_tokens=True)
        return response
    except Exception as e:
        print("Error in generating response:", e)
        return "I'm sorry, I couldn't generate a response."


