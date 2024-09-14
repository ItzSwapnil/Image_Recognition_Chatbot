# Conversational AI with Image Recognition

This project is a conversational AI application that integrates image recognition capabilities. It uses a pre-trained model from the `transformers` library to generate responses based on user queries and images.

## Features

- Load and display images
- Send text queries along with images
- Receive AI-generated responses based on the input image and query
- GUI built with Tkinter


## Usage

1. Run the GUI application:
    ```sh
    python gui.py
    ```

2. Use the GUI to load an image, enter a query, and get a response from the AI.

## Project Structure

- `app.py`: Contains the core logic for loading the model and processing images and queries.
- `gui.py`: Implements the graphical user interface using Tkinter.
- `.gitignore`: Specifies files and directories to be ignored by Git.

## Dependencies

- `transformers`
- `torch`
- `Pillow`
- `tkinter`

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Acknowledgements

- [Hugging Face Transformers](https://github.com/huggingface/transformers)
- [PyTorch](https://pytorch.org/)
- [Pillow](https://python-pillow.org/)
- [Tkinter](https://docs.python.org/3/library/tkinter.html)
- [Qwen2-VL-7B-Instruct](https://huggingface.co/Qwen/Qwen2-VL-7B-Instruct)