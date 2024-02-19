import os
from functools import partial
from flask_migrate import Migrate
from app import create_app, db, scheduler
from app.services.scheduled_budget_check import scheduled_budget_check

app = create_app()
partial_func = partial(scheduled_budget_check, app=app)
migrate = Migrate(app, db)


port = int(os.environ.get("PORT", 8000))

if __name__ == "__main__":
    scheduler.add_job(id='Scheduled Task', func=partial_func,
                      trigger='interval', minutes=1)
    app.run(debug=True, port=port)
