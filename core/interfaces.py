from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class BotConfig:
    name: str
    sources: list
    prompt_path: str
    webhook_url: str
    avatar_url: str


class Fetcher(ABC):
    @abstractmethod
    def fetch(self, sources: list) -> str:
        pass


class Analyst(ABC):
    @abstractmethod
    def analyze(self, content: str, prompt_path: str) -> str:
        pass


class Notifier(ABC):
    @abstractmethod
    def notify(self, content: str, config: BotConfig) -> str:
        pass


class Bot:
    def __init__(self, config: BotConfig, fetcher: Fetcher, analyst: Analyst, notifier: Notifier):
        self.config = config
        self.fetcher = fetcher
        self.analyst = analyst
        self.notifier = notifier

    def run(self) -> str:
        print(f"[{self.config.name}] Starting pipeline...")

        content = self.fetcher.fetch(self.config.sources)
        if not content:
            return f"[{self.config.name}] No content fetched"

        analysis = self.analyst.analyze(content, self.config.prompt_path)
        result = self.notifier.notify(analysis, self.config)

        print(f"[{self.config.name}] Pipeline complete: {result}")
        return result
