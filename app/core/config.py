import os


class Settings:
    def __init__(self) -> None:
        self.DATABASE_URL = os.getenv("DATABASE_URL")
        self.WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

        self._validate()

    def _validate(self) -> None:
        if not self.DATABASE_URL:
            raise RuntimeError("DATABASE_URL is not set")

        if not self.WEBHOOK_SECRET:
            raise RuntimeError("WEBHOOK_SECRET is not set")


settings = Settings()




