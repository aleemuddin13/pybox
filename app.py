from flask import Flask, request, jsonify
import subprocess
import json
import os
import re
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

app.config['DEBUG'] = False

# NSJail configuration file path
NSJAIL_CONFIG_PATH = os.path.abspath("./nsjail.cfg")

TEMPLATE_PATH = os.path.abspath("./template.py")
TEMPLATE_PLACE_HOLDER = "# INSERT MAIN HERE"
SCRIPT_PATH = os.path.abspath("./tmp/temp_script.py")



def generate_script(script):
    # Read the content of the file
    with open(TEMPLATE_PATH, 'r') as file:
        content = file.read()

    # Replace the placeholder with the new function
    if TEMPLATE_PLACE_HOLDER in content:
        content = content.replace(TEMPLATE_PLACE_HOLDER, script)
        print("Function inserted successfully.")
    else:
        print(f"Placeholder '{TEMPLATE_PLACE_HOLDER}' not found in the file.")
        return False

    # Write the modified content back to the file
    with open(SCRIPT_PATH, 'w') as file:
        file.write(content)

    return True


def execute_script():
    cmd = f"nsjail  --config {NSJAIL_CONFIG_PATH} -- /usr/local/bin/python {SCRIPT_PATH}"

    # Use NSJail to safely run the script
    process = subprocess.run(cmd.split(), capture_output=True, text=True)
    if process.returncode:
        return {"success": False, "stderr": process.stderr, "stdout": process.stdout}

    print(process.stdout)
    print(process.stderr)
    
    # JSON result will always be last line in stdout.
    stdout_line = process.stdout.splitlines()
    response = json.loads(stdout_line[-1])
    response["stdout"] = "\n".join(stdout_line[:-1])
    response["stderr"] = process.stderr + response.get("stderr", "")
    return response

@app.route('/')
def hello():
    return 'Hello, World!'


@app.route('/execute', methods=['POST'])
def execute():
    # Input validation
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    
    data = request.json
    
    if 'script' not in data or not isinstance(data['script'], str):
        return jsonify({"error": "Invalid script provided"}), 400

    script = data.get('script', '')

    # main function validations
    # Check if the script starts & ends with "def main()"
    if not script.strip().startswith("def main()"):
        return jsonify({"error": "The script must starts with main() function."}), 400
    
    if re.search(r'\n\S', script):
        return jsonify({"error": "The script must contain only main() function."}), 400
    
    # generate temp_script from input
    try:
        generate_result = generate_script(script)
        if not generate_result:
            return jsonify({"error": "Unable to create script"}), 500
    except Exception as e:
        print(f'error: {e}')
        return jsonify({"error": ""}), 500

    # execute script
    try:
        response = execute_script()
        status = 200 
        if not response["success"]:
            status = 400
        return jsonify(response), status
    except Exception as e:
        print(f'error: {e}')
        return jsonify({"error": ""}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
