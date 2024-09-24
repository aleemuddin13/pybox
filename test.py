import requests
import json

API_URL = "http://localhost:8080/execute"

def send_request(script, env=None):
    payload = {"script": script}
    if env:
        payload["env"] = env
    response = requests.post(API_URL, json=payload)
    return response.status_code, response.json()

def run_test(name, script, env=None, expected_status=200, expected_content=None):
    print(f"\nRunning test: {name}")
    status, result = send_request(script, env)
    print(f"Status: {status}")
    print(f"Result: {json.dumps(result, indent=2)}")
    assert status == expected_status, f"Expected status {expected_status}, got {status}"
    if expected_content:
        for key, value in expected_content.items():
            assert key in result, f"Expected key '{key}' not found in response"
            assert result[key] == value, f"Expected '{key}' to be {value}, got {result[key]}"

# Test 1: Basic functionality
run_test("Basic Functionality", "\
def main():\n\
    return 'hello'\n\
    return {\"message\": \"Hello, World!\"}\
", expected_status=200, expected_content={"result": {"message": "Hello, World!"}})


# Test 2: Attempt to access source code files
run_test("Check if source code files are visible",
"def main():\n\
    return {\"files\": os.listdir(\"/app\")}", 
expected_status=200, expected_content={
  "result": {
    "files": [
      "tmp"
    ]
  },
  "stdout": "",
  "success": True
})

#Test 3: Attempt to write to file system
run_test("Allow to write in /tmp", 
"def main():\n\
    with open('/tmp/test.txt', 'w') as f:\n\
        f.write('this is test')\n\
    with open('/tmp/test.txt', 'r') as f:\n\
        print(f.read())\n\
    return {\"message\": \"File written\"}",
    expected_status=200,  expected_content={
  "result": {
    "message": "File written"
  },
  "stdout": "this is test",
  "success": True
})

# Test 4: Don't allow to write except /tmp folder
run_test("Don't allow to write except /tmp", 
"def main():\n\
    with open('/etc/test', 'w') as f:\n\
        f.write('this is test')\n\
    with open('/etc/test', 'r') as f:\n\
        print(f.read())\n\
    return {\"message\": \"File written\"}",
    expected_status=400)


# Test 5: Long-running script (should timeout)
run_test("Long-running script",
"def main():\n\
    import time\n\
    time.sleep(60)\n\
    return {\"content\": \"Finished\"}\n", 
expected_status=400)

# Test 6:  Large memory allocation
run_test("Large memory allocation",
"def main():\n\
    large_list = [0] * (1024 * 1024 * 1024)\n\
    return {\"message\": \"Memory allocated\"}\n", 
expected_status=400)


# Test 7:  Attempt to use networking
run_test("Attempt to use networking",
"def main():\n\
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\n\
    s.connect((\"www.example.com\", 80))\n\
    return {\"message\": \"network connected\"}\n", 
expected_status=400)


print("\nAll tests completed.")