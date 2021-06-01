from .controller.route_controller import mpk
from .csv_importer.import_csv import importer
from .app import app

app.register_blueprint(mpk)
app.register_blueprint(importer)


