import os
from dotenv import load_dotenv
from pathlib import Path

dir_path = os.path.dirname(os.path.realpath(__file__))

env_path = Path(dir_path + "/../../../") / ".env"

load_dotenv(dotenv_path=env_path, verbose=1)