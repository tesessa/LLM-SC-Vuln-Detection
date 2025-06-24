import sys
import yaml

from utils import Struct
from google import genai
from google.genai.types import HttpOptions

# this is a basic call to vetexAI I just looked up, can be changed however you want
def load_model(config):
    client = genai.Client(http_options=HttpOptions(api_version="v1"))
    response = client.models.generate_content(
        model= config.model_name,
        contents= "How does AI work?",
    )
    print(response.text)

if __name__ == "__main__":
    args = sys.argv
    config_path = args[1]

    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    config = Struct(**config)

    load_model(config)