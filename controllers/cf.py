import req
from core.configurations import Configuration, ConfigurationRepository
from flask import Flask, request
from res import BizException, Codes, R


class ConfigFileController:
    def __init__(self,
                 app: Flask,
                 repository: ConfigurationRepository):
        self.app = app
        self.repository = repository
        self.register_routes()

    def register_routes(self):
        """
        Register routes.
        """
        default_name = 'empty'

        @self.app.route('/cf/save', methods=['POST'])
        def save():
            request_body = req.get_json_body()
            print(f'Request Body: {request_body}')

            namespace = request_body.get('namespace', default_name)
            app_name = request_body.get('app_name', default_name)
            hostname = request_body.get('hostname', default_name)
            env = request_body.get('env', default_name)
            name = request_body.get('name', '')
            content = request_body.get('content', '')
            if name == '' or content == '':
                raise BizException.from_codes(Codes.ARGS_ERROR)

            configuration = Configuration(namespace=namespace, app_name=app_name, hostname=hostname, env=env, name=name,
                                          content=content)
            self.repository.save(configuration)
            return R.ok(configuration).json_response()

        @self.app.route('/cf/read', methods=['GET'])
        def read():
            namespace = request.args.get('namespace', default_name)
            app_name = request.args.get('app_name', default_name)
            hostname = request.args.get('hostname', default_name)
            env = request.args.get('env', default_name)
            name = request.args.get('name', '')
            if name == '':
                raise BizException.from_codes(Codes.ARGS_ERROR)

            configuration = self.repository.get(namespace, app_name, hostname, env, name)
            return R.ok(configuration).json_response()
