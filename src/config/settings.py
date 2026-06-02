from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    service_name: str = "web-scraper"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = True
    environment: str = "default"
    postgresql_host: str = "localhost"
    postgresql_port: str = "5432"
    postgresql_db_name: str = "web_scraper"
    postgresql_user: str = "cluster_user"
    postgresql_password: str = ""
    db_pool_size: int = 2
    db_max_overflow: int = 3
    max_concurrent_scrapers: int = 5
    scraper_timeout: int = 30
    otel_endpoint: str = "http://localhost:4317"

    @property
    def database_url(self) -> str:
        return f"{self.postgresql_user}:{self.postgresql_password}@{self.postgresql_host}:{self.postgresql_port}/{self.postgresql_db_name}"


settings = Settings()
