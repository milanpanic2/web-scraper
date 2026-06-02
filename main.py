import uvicorn

from src.config.settings import settings


def main():
    uvicorn.run(
        app="src.api.app:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug
    )


if __name__ == "__main__":
    main()
