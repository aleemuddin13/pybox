## Installation
Clone the repository and build the docker image to set up the project:

```bash
git clone https://github.com/aleemuddin13/pybox.git
cd pybox
docker build -t pybox-exec .
```

## Usage
To run the project in development locally:
```bash
docker run --privileged  -p 8080:8080 pybox-exec
```
OR

```bash
docker run --privileged  -e PYTHONUNBUFFERED=1  -p 8080:8080 -v "$(pwd):/app" pybox-exec
```

## Curl Demo Examples 
replace url with http://localhost:8080/execute if you want to test locally
#### 1. Basic Functionality:
```bash
curl -X POST http://ec2-3-18-20-157.us-east-2.compute.amazonaws.com:8080/execute \
    -H "Content-Type: application/json" \
    -d '{"script": "def main():\n    return {\"message\": \"Hello, World!\"}"}'
```
#### 2. Attempt to Access Application Files 
Should Only Show /tmp Directory
```bash
curl -X POST http://ec2-3-18-20-157.us-east-2.compute.amazonaws.com:8080/execute \
    -H "Content-Type: application/json" \
    -d '{"script": "def main():\n    return {\"files\": os.listdir(\"/app\")}\n"}'
```
#### 3. Write and Read Operations in /tmp Directory
```bash
curl -X POST http://ec2-3-18-20-157.us-east-2.compute.amazonaws.com:8080/execute \
    -H "Content-Type: application/json" \
    -d '{"script": "def main():\n    with open(\"/tmp/test.txt\", \"w\") as f:\n        f.write(\"this is test\")\n    with open(\"/tmp/test.txt\", \"r\") as f:\n        print(f.read())\n    return {\"message\": \"File written\"}"}'
```
#### 4. Prevent Writing Outside /tmp Directory
should return error
```bash
curl -X POST http://ec2-3-18-20-157.us-east-2.compute.amazonaws.com:8080/execute \
    -H "Content-Type: application/json" \
    -d '{"script": "def main():\n    with open(\"/etc/test\", \"w\") as f:\n        f.write(\"this is test\")\n    with open(\"/etc/test\", \"r\") as f:\n        print(f.read())\n    return {\"message\": \"File written\"}"}'

```
#### 5: Handling Long-Running Scripts (Timeout Expected)
Default timeout is 10secs
```bash
curl -X POST http://ec2-3-18-20-157.us-east-2.compute.amazonaws.com:8080/execute \
    -H "Content-Type: application/json" \
    -d '{"script": "def main():\n    import time\n    time.sleep(60)\n    return {\"content\": \"Finished\"}"}'

```
####  6: Restrict Large Memory Allocations
```bash
curl -X POST http://ec2-3-18-20-157.us-east-2.compute.amazonaws.com:8080/execute \
    -H "Content-Type: application/json" \
    -d '{"script": "def main():\n    large_list = [0] * (1024 * 1024 * 1024)\n    return {\"message\": \"Memory allocated\"}"}'
```
#### 7: Prevent Network Access
```bash
curl -X POST http://ec2-3-18-20-157.us-east-2.compute.amazonaws.com:8080/execute \
    -H "Content-Type: application/json" \
    -d '{"script": "def main():\n    import socket\n    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\n    s.connect((\"www.example.com\", 80))\n    return {\"message\": \"network connected\"}"}'

```
