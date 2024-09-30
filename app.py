import torch
from transformers import Qwen2VLForConditionalGeneration, AutoProcessor
from PIL import Image
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Load the model and processor
try:
    model = Qwen2VLForConditionalGeneration.from_pretrained(
        "Qwen/Qwen2-VL-7B-Instruct", torch_dtype=torch.float16 if torch.cuda.is_available() else "auto", device_map=None
    )
    model.to(device=torch.device("cuda" if torch.cuda.is_available() else "cpu"))
    processor = AutoProcessor.from_pretrained("Qwen/Qwen2-VL-7B-Instruct")
except Exception as e:
    logging.error(f"Error loading model or processor: {e}")
    exit(1)

def chat_with_image(image_path, query):
    try:
        image = Image.open(image_path)
        image = image.resize((224, 224))
    except Exception as e:
        logging.error(f"Error opening image: {e}")
        return None

    messages = [
        {
            "role": "user",
            "content": [
                {"type": "image", "image": image},
                {"type": "text", "text": query},
            ],
        }
    ]

    try:
        text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        image_inputs, video_inputs = processor(images=[image], return_tensors="pt")
        inputs = processor(text=[text], images=image_inputs, videos=video_inputs, padding=True, return_tensors="pt")
        inputs = inputs.to(device=torch.device("cuda" if torch.cuda.is_available() else "cpu"))
        with torch.no_grad():
            torch.cuda.empty_cache()
            generated_ids = model.generate(**inputs, max_new_tokens=128)

        generated_ids_trimmed = [
            out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
        ]
        output_text = processor.batch_decode(
            generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
        )[0]

        return output_text
    except Exception as e:
        logging.error(f"Error during processing: {e}")
        return "An error occurred during processing."
