import requests
import json
import os
import time

def load_config():
    """
    Load config file looking into multiple locations
    """
    config_locations = [
        "./_config",
        "prompt-eng/_config",
        "../_config"
    ]
    
    # Find CONFIG
    config_path = None
    for location in config_locations:
        if os.path.exists(location):
            config_path = location
            break
    
    if not config_path:
        raise FileNotFoundError("Configuration file not found in any of the expected locations.")
    
    # Load CONFIG
    with open(config_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()


def create_payload(model, prompt, target="ollama", **kwargs):
    """
    @NOTE: 
    Need to adjust here to support multiple target formats
    target can be only ('ollama' or 'open-webui')
    """
    payload = None
    if target == "ollama":
        payload = {
            "model": model,
            "prompt": prompt, 
            "stream": False,
        }
        if kwargs:
            payload["options"] = {key: value for key, value in kwargs.items()}

    elif target == "open-webui":
        payload = {
            "model": model,
            "messages": [ {"role" : "user", "content": prompt } ]
        }

        payload.upload({key: value for key, value in kwargs.items()})
    
    else:
        print(f'!!ERROR!! Unknown target: {target}')
    return payload


def model_req(payload=None):
    """
    COMPLETE
    """
        
    # CUT-SHORT Condition
    try:
        load_config()
    except:
        return -1, f"!!ERROR!! Problem loading prompt-eng/_config"

    url = os.getenv('URL_GENERATE', None)
    api_key = os.getenv('API_KEY', None)
    delta = response = None

    headers = dict()
    headers["Content-Type"] = "application/json"
    if api_key: headers["Authorization"] = f"Bearer {api_key}"

    #print(url, headers)
    #print(payload)

    # Send out request to Model Provider
    try:
        start_time = time.time()
        response = requests.post(url, data=json.dumps(payload) if payload else None, headers=headers)
        delta = time.time() - start_time
    except:
        return -1, f"!!ERROR!! Request failed! You need to adjust prompt-eng/config with URL({url})"

    # Checking the response and extracting the 'response' field
    if response is None:
        return -1, f"!!ERROR!! There was no response (?)"
    elif response.status_code == 200:

        ## @NOTE: Need to adjust here to support multiple response formats
        result = ""
        delta = round(delta, 3)

        response_json = response.json()
        if 'response' in response_json: ## ollama
            result = response_json['response']
        elif 'choices' in response_json: ## open-webui
            result = response_json['choices'][0]['message']['content']
        else:
            result = response_json 
        
        return delta, result
    elif response.status_code == 401:
        return -1, f"!!ERROR!! Authentication issue. You need to adjust prompt-eng/config with API_KEY ({url})"
    else:
        return -1, f"!!ERROR!! HTTP Response={response.status_code}, {response.text}"
    return


###
### DEBUG
###

if __name__ == "__main__":
    from _pipeline import create_payload, model_req
    MESSAGE = "Step 1: Generate a list of potential data sources for stock sentiment analysis (e.g., Twitter, news articles, Reddit, financial reports). Step 2: Identify the key financial metrics that influence stock overvaluation. Step 3: Based on steps 1 and 2, define the system requirements for an AI tool that integrates sentiment and fundamental analysis."
    PROMPT = MESSAGE 
    num_ctx_range = [1000, 10000, 50000, 100000]
    num_predict_range = [1000, 10000, 50000, 100000]
    results = []
    for num_ctx in num_ctx_range:
        for num_predict in num_predict_range:      
            payload = create_payload(
                                 target="ollama",   
                                 model="qwen2.5:0.5B", 
                                 prompt=PROMPT, 
                                 temperature=.5, 
                                 num_ctx=num_ctx, 
                                 num_predict=num_predict)

            time, response = model_req(payload=payload)
            print(response)
            if time: 
                print(f"Running with num_ctx = {num_ctx} and num_predict = {num_predict}")
                print(f'Time taken: {time}s\n\n')
                results.append((num_ctx, num_predict, time))

    print("Summary of results:")
    for num_ctx, num_predict, time in results:
        print(f"num_ctx = {num_ctx}, num_predict = {num_predict}, Time taken = {time}s")
