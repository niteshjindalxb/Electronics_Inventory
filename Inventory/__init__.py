from flask import Flask
from .views import createApp

app = createApp()

from . import urls
urls.set_urls()

# app.run(debug=True)