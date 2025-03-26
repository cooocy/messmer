from config.loader import load_yaml_configurations

app_configurations = load_yaml_configurations('config/app.yaml')

__all__ = ['app_configurations']
