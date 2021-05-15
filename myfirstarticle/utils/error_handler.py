from flask import jsonify


def handle_errors(app):
    @app.errorhandler(422)
    def validation_error(err):
        messages = err.data.get('messages').get('json')
        response = {"status": "failed", "messages": messages}
        return jsonify(response), 422
