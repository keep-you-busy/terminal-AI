
from dynaconf import Dynaconf

settings = Dynaconf(
    root_path='config/',
    envvar_prefix='TERMINAL_AI',
    settings_files=['settings.yaml', '.secrets.yaml'],
    yaml_loader='safe_load',
)
