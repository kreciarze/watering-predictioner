import os
from datetime import datetime
from config import SAVE_LOG_DIR

today = datetime.today().strftime('%Y_%m_%d')
def log_response(should_water: bool) -> None:
    with open(f'{SAVE_LOG_DIR}/log_{today}.csv', "a") as f:
        f.write(f"{datetime.now()},{should_water}\n")
    return