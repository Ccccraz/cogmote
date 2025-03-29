from dataclasses import dataclass, field
from pydantic import BaseModel, ValidationError
from pathlib import Path

import json
import os
import appdirs

from puremote.common.logger import logger


@dataclass(eq=True)
class FigureConfig:
    nickname: str
    x_axis: str
    y_axis: str
    figure_type: str


@dataclass
class TrialDataConfig:
    nickname: str
    address: str
    mode: str = "sse"
    data_labels: list[str] = field(default_factory=list)
    figures: list[FigureConfig] = field(default_factory=list)


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
    """

    video_source: dict[str, str] = {}
    trial_data: list[TrialDataConfig] = []


APP_NAME = "puremote"
CONFIG_FILE_PATH = Path(
    os.getenv(
        "CONFIG_FILE_PATH", Path(appdirs.user_config_dir(APP_NAME)).with_suffix(".json")
    )
)


class Configure:
    def __init__(self):
        self.config = self._load_config()

        self.trial_data_address = {
            trial_data.address: trial_data for trial_data in self.config.trial_data
        }

        self.trial_data_nickname = {
            trial_data.nickname: trial_data for trial_data in self.config.trial_data
        }

    def _create_default_config(self) -> ConfigModel:
        config = ConfigModel()
        try:
            CONFIG_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)

            with CONFIG_FILE_PATH.open("w") as f:
                json.dump(config.model_dump(), f, indent=4)

            return config
        except IOError:
            logger.error("Failed to create configuration file")
        finally:
            return config

    def _load_config(self) -> ConfigModel:
        # Check if the file exists
        if not os.path.exists(CONFIG_FILE_PATH):
            logger.info("Configuration file not found")
            logger.info(f"Creating default configuration file at {CONFIG_FILE_PATH}")
            return self._create_default_config()

        # Check if the file is readable
        if not os.access(CONFIG_FILE_PATH, os.R_OK):
            logger.warning("No permission to read the configuration file")
            logger.warning(
                f"Trying to switch to default configuration file at {CONFIG_FILE_PATH}"
            )
            return self._create_default_config()

        try:
            with open(CONFIG_FILE_PATH, "r") as f:
                logger.info(f"Loading configuration file from {CONFIG_FILE_PATH}")
                return ConfigModel(**json.load(f))
        except json.JSONDecodeError:
            logger.error("Configuration file format error")
            return self._create_default_config()
        except ValidationError as e:
            logger.error(f"Configuration file is invalid: {e}")
            return self._create_default_config()

    def _save(self):
        try:
            with open(CONFIG_FILE_PATH, "w") as f:
                json.dump(self.config.model_dump(), f, indent=4)
        except IOError:
            logger.error("Failed to write configuration file")

    def add_trial_data(self, trial_data: TrialDataConfig) -> None:
        if trial_data.address in self.trial_data_address:
            logger.warning(
                f"Trial data with address {trial_data.address} already exists"
            )
            return

        self.config.trial_data.append(trial_data)

        self.trial_data_address[trial_data.address] = trial_data
        self.trial_data_nickname[trial_data.nickname] = trial_data

        self._save()

    def add_figure(self, address: str, figure: FigureConfig) -> None:
        if address not in self.trial_data_address:
            logger.warning(f"Trial data with address {address} does not exist")
            return

        figures = self.trial_data_address[address].figures

        if figure in figures:
            logger.warning(f"Figure {figure.nickname} already exists")
            return

        figures.append(figure)
        self._save()


config_store = Configure()

if __name__ == "__main__":
    config = Configure()
    logger.info(config.config.model_dump_json(indent=4))
