from functools import partial
from app import create_app, db, scheduler
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from main import scheduled_check_budget

app = create_app()
partial_func = partial(scheduled_check_budget, app=app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

if __name__ == "__main__":
    scheduler.add_job(id='Scheduled Task', func=partial_func,
                      trigger='interval', minutes=1)
    app.run(debug=True)



# def list_routes(app):
#     """
#     Function to list all registered routes in a Flask app.
#     """
#     output = []
#     for rule in app.url_map.iter_rules():
#         methods = ','.join(rule.methods)
#         line = f"{rule.endpoint} : {methods} : {rule}"
#         output.append(line)
#     return output

# Call the function to list routes and print them
# routes = list_routes(app)
# for route in routes:
#     print(route)
