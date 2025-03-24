import yaml

from controllers.cf import ConfigFileController
from core.configurations import ConfigurationRepository
from flask import Flask, jsonify
from responses.exceptions import BizException, Codes
from responses.results import R


def load_yaml_configurations(config_path):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config


app_configurations__ = load_yaml_configurations('config/app.yaml')
repository = ConfigurationRepository(app_configurations__)
app = Flask('Messmer')
cf_controller = ConfigFileController(app, app_configurations__, repository)


@app.route('/')
def hello_world():  # put application's code here
    r = R.ok('Hello! This is Messmer.')
    return jsonify(r)


@app.errorhandler(Exception)
def handle_exception(e):
    """
    Global Exceptions Handler.
    """

    if not isinstance(e, BizException):
        # Other exception, convert to bizException and then return.
        # TODO log
        print(e)
        e = BizException.from_codes(Codes.SERVER_ERROR)

    r = R.error(e)
    return jsonify(r), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=app_configurations__['server']['port'], debug=False)
