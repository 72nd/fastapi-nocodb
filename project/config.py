import typed_settings as ts


@ts.settings
class Settings:
    port: int
    """Port for the web-server"""
    proxy_headers: bool
    """Whether Uvicorn should provide proxy headers"""
    log_level: str
    """Logging level for the application."""
    dev_mode: bool
    """
    Whether application should run in development mode or not. This currently only enables
    Uvicorn's auto reload.
    """
    nocodb_api_key: str = ts.secret()
    """API Key for the NocoDB instance."""


settings = ts.load(Settings, appname="project", config_files=["settings.toml", ".secrets.toml"])