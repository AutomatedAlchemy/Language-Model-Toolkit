import os


class cls_python_code_api:
    def __init__(self, filename):
        """Initialize with a specified filename."""
        self.filename = filename

    def create_script(self, script_contents):
        """Create a new script with provided contents. Returns a message."""
        try:
            with open(self.filename, 'w') as file:
                file.write(script_contents)
            return f"Script created successfully."
        except Exception as e:
            return f"Error: {e}"

    def read_script(self):
        """Read and return script contents as a string or an error message."""
        try:
            with open(self.filename, 'r') as file:
                return file.read()
        except FileNotFoundError:
            return f"File not found. Please create a script first."
        except Exception as e:
            return f"Error: {e}"

    def edit_script(self, new_contents):
        """Edit the script with new contents. Returns a message."""
        try:
            with open(self.filename, 'r') as file:
                script_contents = file.read()
            
            if new_contents:
                with open(self.filename, 'w') as file:
                    file.write(new_contents)
                return "Script updated successfully."
            else:
                return "No changes made."

        except FileNotFoundError:
            return f"File not found. Please create a script first."
        except Exception as e:
            return f"Error: {e}"

    def execute_script(self):
        """Execute the script. Returns a message."""
        try:
            with open(self.filename, 'r') as file:
                script_contents = file.read()
            
            exec(script_contents)
            return "Script executed successfully."
        except FileNotFoundError:
            return f"File not found. Please create a script first."
        except Exception as e:
            return f"Error: {e}"