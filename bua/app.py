from flask_admin.contrib.sqla import ModelView

from bua import create_app, db
from bua.models import admin, Squad, Task

app = create_app()
admin.add_view(ModelView(Task, db.session))

if __name__ == '__main__':
    app.run(debug=True)
