from core import Bot, RSSFetcher, OpenAIAnalyst, DiscordNotifier


class BotRegistry:
    _bots: dict = {}
    _initialized: bool = False

    @classmethod
    def _ensure_initialized(cls):
        if cls._initialized:
            return

        from bots.sisa_go.config import config as sisa_go_config
        cls._bots["sisa-go"] = sisa_go_config
        cls._initialized = True

    @classmethod
    def get(cls, name: str) -> Bot:
        cls._ensure_initialized()

        if name not in cls._bots:
            raise KeyError(f"Bot '{name}' not found. Available: {list(cls._bots.keys())}")

        config = cls._bots[name]
        return Bot(config, RSSFetcher(), OpenAIAnalyst(), DiscordNotifier())

    @classmethod
    def list_bots(cls) -> list:
        cls._ensure_initialized()
        return list(cls._bots.keys())


def get_bot(name: str) -> Bot:
    return BotRegistry.get(name)
