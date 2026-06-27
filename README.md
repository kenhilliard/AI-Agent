# AI Agent

A Python-based AI agent that uses the Gemini API to autonomously
read, analyze, and fix bugs in a codebase.

## Features

- Reads and writes files from the filesystem
- Executes Python code to test fixes
- Uses function calling to interact with the codebase
- Iteratively works through problems until resolved

## Usage

Set your Gemini API key as an environment variable:

```bash
export GEMINI_API_KEY=your_api_key_here

Then run the agent:

python main.py "your prompt here"

## Warning
This is a toy project for learning purposes. Do not use it in
production or grant it access to sensitive files.
