# IMPORT COMMON LIBRARIES FOR SCRIPT
import os
import pandas as pd
import numpy as np
import json
import socket

# INSERT MAIN HERE

if __name__ == "__main__":
    output = {"success": True}
    try:
        data = main()
        parsed = json.loads(json.dumps(data))
        if not isinstance(parsed, (dict, list)):
            raise Exception("main should return json output")
        output["result"] = data
    except (ValueError, TypeError, json.JSONDecodeError):
        output["success"] = False
        output["stderr"]  = f"The main() function did not return a valid JSON: {data}"
    except Exception as e:
        output["success"] = False
        output["stderr"]  = f"Error: {e}"
    print(json.dumps(output))

