import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file in the specified directory relative to the working directory",
    parameters=types.Schema(required=["file_path"],
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to be executed, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY, items=types.Schema(type=types.Type.STRING),
                description="Arguments to pass to the Python file",
            ),
        },
    ),
)

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        abs_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        # Will be True or False
        valid_file_path = os.path.commonpath([working_dir_abs, abs_file_path]) == working_dir_abs
        if not valid_file_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        command = ["python", abs_file_path]
        if args is not None:
            command.extend(args)
        result = subprocess.run(
            command, capture_output=True, text=True, cwd=working_dir_abs, timeout=30,
        )
        output = ""
        if result.returncode != 0:
            output += f"Process exited with code {result.returncode}\n"
        if result.stdout:
            output += f"STDOUT: {result.stdout}"
        if result.stderr:
            output += f"STDERR: {result.stderr}"
        if not result.stdout and not result.stderr:
            output += "No output produced"
        return output
        
    except Exception as e:
        return f"Error: executing Python file: {e}"
