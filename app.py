from transformers import Qwen2VLForConditionalGeneration, AutoProcessor
from qwen_vl_utils import process_vision_info
import torch
from PIL import Image

# use cuda if available
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load the model
try:
    model = Qwen2VLForConditionalGeneration.from_pretrained(
        "Qwen/Qwen2-VL-7B-Instruct", torch_dtype=torch.float16 if device == "cuda" else "auto", device_map=None
    )
    model.to(device)
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

# Default processor
try:
    processor = AutoProcessor.from_pretrained("Qwen/Qwen2-VL-7B-Instruct")
except Exception as e:
    print(f"Error loading processor: {e}")
    processor = None

conversation_history = []


def chat_with_image(image_path, query, history=[]):
    if model is None or processor is None:
        print("Model or processor not initialized correctly.")
        return None, history

    try:
        image = Image.open(image_path)
        # memory load reducer
        image = image.resize((224, 224))
    except Exception as e:
        print(f"Error opening image: {e}")
        return None, history

    messages = history + [
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "image": image,
                },
                {"type": "text", "text": query},
            ],
        }
    ]

    try:
        # UI: Inference
        text = processor.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        image_inputs, video_inputs = process_vision_info(messages)
        inputs = processor(
            text=[text],
            images=image_inputs,
            videos=video_inputs,
            padding=True,
            return_tensors="pt",
        )
        # Move inputs to the same device as the model
        inputs = inputs.to(device)
        # Inference: Generation of the output
        with torch.no_grad():
            torch.cuda.empty_cache()  # Clear CUDA cache
            generated_ids = model.generate(**inputs, max_new_tokens=128)

        generated_ids_trimmed = [
            out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
        ]
        output_text = processor.batch_decode(
            generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
        )[0]

        history.append({
            "role": "assistant",
            "content": {"type": "text", "text": output_text}
        })

        return output_text, history
    except Exception as e:
        print(f"Error during processing: {e}")
        return "An error occurred during processing.", history


# Example usage (for testing)
if __name__ == "__main__":
    image_path = "swapnil.jpg"
    query = "Describe this image."
    response, conversation_history = chat_with_image(image_path, query, conversation_history)
    print(response)