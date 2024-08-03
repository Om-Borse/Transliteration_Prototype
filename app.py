from flask import Flask, request, jsonify, send_from_directory
from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch

app = Flask(__name__, static_folder='static', template_folder='templates')

# Load the saved model and tokenizer
model = T5ForConditionalGeneration.from_pretrained('./static')
tokenizer = T5Tokenizer.from_pretrained('./static')

# Ensure the model is in evaluation mode
model.eval()

@app.route('/')
def index():
    """Serve the HTML file."""
    return send_from_directory('templates', 'index.html')

@app.route('/translate', methods=['POST'])
def translate():
    """Translate Hinglish text to English."""
    data = request.get_json()
    text = data.get('text', '')
    
    # Prepare the input text
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding='max_length', max_length=128)
    input_ids = inputs["input_ids"].to(model.device)
    
    # Generate translation
    with torch.no_grad():
        outputs = model.generate(input_ids, max_length=128, num_beams=4, early_stopping=True)
    
    # Decode the output and return
    translation = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return jsonify({'translation': translation})

if __name__ == '__main__':
    app.run(port=5000)