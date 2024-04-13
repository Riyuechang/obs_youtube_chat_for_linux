import yaml

class Config:
    def __init__(self, config_path: str) -> None:
        with open(config_path, "r", encoding="utf-8") as file:
            config_data: dict = yaml.safe_load(file)

        self.youtube_channel_id = config_data["youtube_channel_id"]


config_path = "config.yml"
config = Config(config_path)