from flask import Flask as FlaskBase
from flask import Blueprint as FlaskBlueprint
from .blueprint import Blueprint

class Flask(FlaskBase):
    def __init__(self, *args, **kwargs):
        print(f'@ Flask.__init__')
        super().__init__(*args, **kwargs)
    def register_blueprint(self, blueprint, **options):
        print(f'@ Flask.register_blueprint(blueprint={blueprint})')
        if isinstance(blueprint, Blueprint):
            print("! not doing anything at the moment")
            blueprint.prepare_routes()
        super().register_blueprint(blueprint, **options)

