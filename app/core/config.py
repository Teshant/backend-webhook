import os


class Settings:
    
    #Central place to load and validate environment variables.
    

    def __init__(self) -> None:
    
        self.DATABASE_URL = os.getenv("DATABASE_URL")
        self.WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")

        
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

        # Validate required variables
        self._validate()

    def _validate(self) -> None:
        
        #Validate required configuration
        
        if not self.DATABASE_URL:
            raise RuntimeError("DATABASE_URL environment variable is not set")

        if not self.WEBHOOK_SECRET:
            raise RuntimeError("WEBHOOK_SECRET environment variable is not set")



settings = Settings()     


