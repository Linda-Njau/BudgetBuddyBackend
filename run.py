from functools import partial
from app import create_app, db, scheduler
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from app.api.services.budget_monitor_service import scheduled_check_budget

app = create_app()
partial_func = partial(scheduled_check_budget, app=app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

if __name__ == "__main__":
    scheduler.add_job(id='Scheduled Task', func=partial_func,
                      trigger='interval', minutes=30)
    app.run(debug=True)



