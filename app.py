from flask import Flask, jsonify

from responses.exceptions import BizException, Codes
from responses.results import R

app = Flask('Messmer')


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
        e = BizException.from_codes(Codes.SERVER_ERROR, e.description)

    r = R.error(e)
    return jsonify(r), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
