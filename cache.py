from functools import lru_cache

import yaml


@lru_cache()
def load_config(config_path='config/base.yaml'):
    with open(config_path, encoding="utf-8_sig") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)

@lru_cache()
def load_secret(config_path='config/secret_template.yaml'):
    with open(config_path, encoding="utf-8_sig") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)

    return data