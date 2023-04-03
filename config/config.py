from dynaconf import Dynaconf

settings = Dynaconf(
    root_path='config/',
    core_loaders=['YAML'],
    default_env='default',
    envvar_prefix='TERMINAL_AI',
    settings_files=['settings.yaml', '.secrets.yaml', 'customization.yaml'],
    # environments=['default', 'development', 'production'],
    yaml_loader='safe_load',
    load_dotenv=False
)
