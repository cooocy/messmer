import config.loader
import filters

from controllers.cf import ConfigFileController
from core.configurations import ConfigurationRepository
from flask import Flask
from res import BizException, Codes, R

app_name__: str = 'Messmer'
app_configurations__: dict = config.loader.load_yaml_configurations('config/app.yaml')
app__ = Flask(app_name__)

filters.register_filters(app__, app_configurations__)

repository = ConfigurationRepository(app_configurations__)
cf_controller = ConfigFileController(app__, app_configurations__, repository)


@app__.errorhandler(Exception)
def handle_exception(e):
    """
    Global Exceptions Handler.
    """

    if not isinstance(e, BizException):
        # Other exception, convert to bizException and then return.
        # TODO log
        print(e)
        e = BizException.from_codes(Codes.SERVER_ERROR)

    return R.error(e).json_response()


@app__.route('/')
def index():
    """
    Health Check.
    """

    r = R.ok(f'Hello! This is {app_name__}.')
    return r.json_response()


if __name__ == '__main__':
    app__.run(host='0.0.0.0', port=app_configurations__['server']['port'], debug=False)
