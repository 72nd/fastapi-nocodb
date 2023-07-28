from .config import settings

import typer
import uvicorn


app = typer.Typer()


@app.command()
def run():
    print(settings)
    uvicorn.run(
        "project.server:app",
        reload=settings.dev_mode,
        port=settings.port,
        proxy_headers=settings.proxy_headers,
        log_level=settings.log_level.lower(),
    )


def main():
    app()


if __name__ == "__main__":
    app()