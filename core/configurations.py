import os.path

from dataclasses import dataclass

from config import app_configurations
from res import BizException, Codes


@dataclass
class Configuration:
    """
    Represents a configuration file.
    """
    namespace: str
    app_name: str
    hostname: str
    env: str
    name: str
    content: str


class ConfigurationRepository:
    """
    Keep the relationship of namespace/app_name/hostname/env/name content.
    """

    def __init__(self):
        self.local_disk_file_storage = LocalDiskFileStorage(app_configurations)

    def save(self, configuration: Configuration):
        """
        TODO sync
        """
        final_key = ConfigurationRepository.__assemble_final_key(configuration)
        self.local_disk_file_storage.storage(final_key, configuration.content)
        return configuration

    def get(self, namespace: str, app_name: str, hostname: str, env: str, name: str) -> Configuration:
        configuration = Configuration(namespace, app_name, hostname, env, name, '')
        final_key = ConfigurationRepository.__assemble_final_key(configuration)
        content = self.local_disk_file_storage.read(final_key)
        configuration.content = content
        return configuration

    @staticmethod
    def __assemble_final_key(configuration: Configuration) -> str:
        return f'{configuration.namespace}#{configuration.app_name}#{configuration.hostname}#{configuration.env}#{configuration.name}'


class LocalDiskFileStorage:
    """
    Storage the configuration content to the local disk.
    """

    def __init__(self, app_configurations: dict):
        self.app_configurations = app_configurations

    def storage(self, storage_key, content: str):
        dir_path = self.app_configurations['configurations']['storage']['path']
        if not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
        file_path = os.path.join(dir_path, storage_key)
        with open(file_path, 'w+', encoding='utf-8') as file:
            file.write(content)

    def read(self, storage_key: str) -> str:
        dir_path = self.app_configurations['configurations']['storage']['path']
        file_path = os.path.join(dir_path, storage_key)
        if not os.path.exists(file_path):
            raise BizException.from_codes(Codes.NOT_FOUND)
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
