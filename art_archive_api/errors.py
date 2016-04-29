from flask import jsonify

from application import app


# Error Response
@app.errorhandler(404)
def page_not_found(error):
    response = jsonify({'error': 'Not Found'})
    response.status_code = 404
    return response

@app.errorhandler(422)
def unprocessable_entity(error):
    response = jsonify({'error': 'Unprocessable Entity'})
    response.status_code = 422
    return response

@app.errorhandler(500)
def internal_server_error(error):
    response = jsonify({'error': 'Internal Server Error'})
    response.status_code = 500
    return response