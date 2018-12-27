"""HTML exceptions."""
from . import app
from flask import render_template


@app.errorhandler(404)
def not_found(error):
    """Define a custom page when a 404 is thrown."""
    return render_template('404.html', error=error), 404
