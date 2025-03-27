from pydantic import BaseModel, ValidationError
from pathlib import Path

import json
import os
import appdirs

from puremote.common.logger import logger


class Figure(BaseModel):
    nickname: str
    x_axis: str
    y_axis: str


class ConfigModel(BaseModel):
    """
    Configuration model class for storing various configuration parameters of the application

    Attributes:
        video_source (Dict[str, str]): Video source configuration
            - key (str): nime of the video source
            - key (str): source path or URL
            - default value: `{}`

        video_monitor_backend (List[str]): List of available video monitoring backends
            - every string in the list represents an available video monitoring backend
            - default value: `["vlc", "opengl"]`。

        trial_data_source (List[Dict[str, str]]): trial data source configuration
            - every dictionary in the list represents a trial data source
            - structure of the dictionary:
                - key (str): nickname of the data source
                - key (str): data source path or URL
            _ default value: `[]`

        trial_data_mode (List[str]): request mode for trial data
            - every item in the list represents an available request mode for trial data
            - default value: `["polling", "sse"]`
    """

    video_source: dict[str, str] = {}
    trial_data_source: list[dict[str, str]] = []
    trial_data_mode: list[str] = ["polling", "sse"]
    figure: list[Figure] = []


APP_NAME = "puremote"
CONFIG_FILE_PATH = Path(
    os.getenv(
        "CONFIG_FILE_PATH", Path(appdirs.user_config_dir(APP_NAME)).with_suffix(".json")
    )
)

class Config:
    def __init__(self):
        self.config = self._load_config()
    
    def _create_default_config(self) -> ConfigModel:
        config = ConfigModel()
        try:
            CONFIG_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)

            with CONFIG_FILE_PATH.open("w") as f:
                json.dump(config.model_dump(), f, indent=4)
                
            return config
        except IOError:
            logger.error("Failed to create configuration file")
            pass
    
    def _load_config(self) -> ConfigModel:
        config: ConfigModel | None = None
        # Check if the file exists
        if not os.path.exists(CONFIG_FILE_PATH):
            logger.info("Configuration file not found")
            logger.info(f"Creating default configuration file at {CONFIG_FILE_PATH}")
            config = self._create_default_config()

        # Check if the file is readable
        if not os.access(CONFIG_FILE_PATH, os.R_OK):
            logger.warning("No permission to read the configuration file")
            return

        try:
            with open(CONFIG_FILE_PATH, "r") as f:
                config_data = json.load(f)

            # Check if the data is valid
            config = ConfigModel(**config_data)
            return config
        except json.JSONDecodeError:
            logger.error("Configuration file format error")
        except ValidationError as e:
            logger.error(f"Configuration file is invalid: {e}")
    
    def save(self):
        if self.config is not None:
            try:
                with open(CONFIG_FILE_PATH, "w") as f:
                    json.dump(self.config.model_dump(), f, indent=4)
            except IOError:
                logger.error("Failed to write configuration file")

if __name__ == "__main__":
    config = Config()
    logger.info(config.get_config().model_dump_json(indent=4))
