# Megaservice LLM Platform - User Guide

Welcome to the Megaservice LLM Platform! This guide will walk you through the features and functionality of the application.

## Overview

The Megaservice LLM Platform provides a user-friendly interface for interacting with Ollama's large language models. The platform allows you to:

- Generate text using various AI models
- Manage and download different Ollama models
- Customize generation parameters

## Getting Started

After [installing the application](./INSTALLATION.md), you can access the web interface at http://localhost:8501 in your browser.

The interface consists of two main tabs:
1. **Text Generation** - Create and generate AI-powered text
2. **Model Management** - View and download models

## Text Generation

The Text Generation tab is the primary interface for creating AI-generated content.

### Composing a Prompt

1. In the **Prompt** box, enter the text you want the AI to respond to.
   - Be specific and clear in your instructions
   - Provide context and examples if needed
   - The more detailed your prompt, the better results you'll get

### Generation Settings

On the right side of the interface, you can customize the generation parameters:

1. **Model** - Select the AI model to use for generation
   - Different models have different capabilities and specializations
   - Some models are smaller and faster, while others are larger and more capable

2. **Temperature** - Adjust the randomness of the generated text (0.1 to 1.0)
   - Lower values (closer to 0.1) produce more focused, deterministic outputs
   - Higher values (closer to 1.0) produce more creative, varied outputs
   - For factual or coding tasks, use lower temperature values
   - For creative writing or brainstorming, use higher temperature values

3. **Max Tokens** - Set the maximum length of the generated text
   - Higher values allow for longer outputs but may take more time to generate

### Generating Text

Once you've entered your prompt and adjusted the settings:

1. Click the **Generate Text** button
2. The system will process your request and display the results in the **Generated Output** section
3. If you want to modify the output, adjust your prompt or settings and generate again

## Model Management

The Model Management tab allows you to view and download different Ollama models.

### Viewing Available Models

1. The **Available Models** section displays all currently downloaded models
2. You can see the model name, size, and last modified date for each model
3. To refresh the list, click the **Refresh Model List** button

### Downloading New Models

1. In the **Download New Model** section, enter the model identifier you want to download
   - Model identifiers can be found at the [Ollama Library](https://ollama.com/library)
   - Examples include: `llama3.2:1b`, `mistral:7b`, etc.
2. Click the **Download Model** button to start the download
3. Downloading models may take several minutes depending on your internet connection and the model size
4. Once downloaded, the model will appear in the **Available Models** list and can be selected in the Text Generation tab

## Tips for Effective Use

### Optimize Your Prompts

- **Be specific**: Clear instructions lead to better results
- **Provide context**: Include relevant background information
- **Use examples**: Show the AI the kind of output you're looking for
- **Iterate**: If you don't get the desired result, refine your prompt and try again

### Choosing the Right Model

- **Smaller models** (1B-7B parameters) are faster but may have limited capabilities
- **Larger models** (13B+ parameters) provide better results but require more resources
- **Specialized models** may perform better for specific tasks (coding, medical text, etc.)

### Managing System Resources

- Large models require significant memory and may slow down your system
- Close other resource-intensive applications when using larger models
- If you experience slow performance, try using a smaller model

## Troubleshooting

### Common Issues

#### Slow Generation Times

- Try using a smaller model
- Reduce the maximum tokens parameter
- Check if other applications are using system resources

#### Poor Quality Output

- Refine your prompt to be more specific
- Try a different (typically larger) model
- Adjust the temperature parameter
- Break complex tasks into smaller, simpler prompts

#### Connection Errors

- Ensure the Ollama server is running
- Check your internet connection
- Verify that the API URL in the configuration is correct

## Feedback and Support

If you encounter issues or have suggestions for improvement, please refer to the project repository for support options.

## Privacy and Data Usage

- All processing happens locally on your machine
- Prompts and generated texts are not stored or shared with external services
- Model downloads are retrieved from the Ollama servers