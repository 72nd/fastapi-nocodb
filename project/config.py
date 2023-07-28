import typed_settings as ts


@ts.settings
class Settings:
    nocodb_api_key: str = ts.secret()
    dev_mode: bool = False


settings = ts.load(Settings, appname="project", config_files=["settings.toml", ".secrets.toml"])

# settings = Dynaconf(
#     envvar_prefix="PR",
#     settings_file=["settings.toml", ".secrets.toml"],
#     validators=[
#         Validator("DEV_MODE", must_exist=True)
#     ],
# )