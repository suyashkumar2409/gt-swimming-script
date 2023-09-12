from functools import lru_cache

import yaml


BASE_CONFIG  = "config/base.yaml"
SECRET_CONFIG = "config/secret.yaml"
@lru_cache()
def load_config(config_path=BASE_CONFIG):
    with open(config_path, encoding="utf-8_sig") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    return data

@lru_cache()
def load_secret(config_path=SECRET_CONFIG):
    with open(config_path, encoding="utf-8_sig") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)

    return data

def update_secret_with_calendar_id(calendar_id):
    data = load_secret()
    data['calendar_id'] = str(calendar_id)
    with open(SECRET_CONFIG, 'w') as file:
        yaml.dump(data, file)