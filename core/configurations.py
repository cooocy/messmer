import os.path

from dataclasses import dataclass


@dataclass
class Configuration(dict):
    """
    Represents a configuration file
    """
    namespace: str
    name: str
    content: str


class ConfigurationRepository:
    """
    Keep the relationship of namespace/name/configuration content.
    """

    def __init__(self, app_configurations__: dict):
        self.app_configurations__ = app_configurations__
        self.local_disk_file_storage = LocalDiskFileStorage(app_configurations__)

    def save(self, namespace: str, name: str, content: str) -> Configuration:
        """
        TODO sync
        """
        configuration = Configuration(namespace, name, content)
        final_key = ConfigurationRepository.__assemble_final_key(configuration)
        self.local_disk_file_storage.storage(final_key, content)
        return configuration

    def get(self, namespace: str, name: str) -> Configuration:
        configuration = Configuration(namespace, name, '')
        final_key = ConfigurationRepository.__assemble_final_key(configuration)
        content = self.local_disk_file_storage.read(final_key)
        configuration.content = content
        return configuration

    @staticmethod
    def __assemble_final_key(configuration: Configuration) -> str:
        return f'{configuration.namespace}#{configuration.name}'


class LocalDiskFileStorage:
    """
    Storage the configuration content to the local disk.
    """

    def __init__(self, app_configurations__: dict):
        self.app_configurations__ = app_configurations__

    def storage(self, storage_key, content: str):
        dir_path = self.app_configurations__['configurations']['storage']['path']
        if not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
        file_path = os.path.join(dir_path, storage_key)
        with open(file_path, 'w+', encoding='utf-8') as file:
            file.write(content)

    def read(self, storage_key: str) -> str:
        dir_path = self.app_configurations__['configurations']['storage']['path']
        file_path = os.path.join(dir_path, storage_key)
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
