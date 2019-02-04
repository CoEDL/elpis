from flask import Flask as FlaskBase
from flask import Blueprint as FlaskBlueprint
from .blueprint import Blueprint

class Flask(FlaskBase):
    def __init__(self, *args, **kwargs):
        print(f'@ Flask.__init__')
        super().__init__(*args, **kwargs)
    def register_blueprint(self, blueprint, **options):
        print(f'@ Flask.register_blueprint(blueprint={blueprint})')
        if not isinstance(blueprint, Blueprint):
            super().register_blueprint(blueprint, **options)
            return
        # Deal with custom Blueprint objects
        blueprint.app = self
        blueprint.prepare_routes()
        blueprint.register_app( lambda bp: super(Flask, self).register_blueprint(bp), self )

