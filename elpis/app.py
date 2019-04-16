from flask import Flask as FlaskBase
from .blueprint import Blueprint


class Flask(FlaskBase):
    """Custom app to allow multi-level blueprints."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def register_blueprint(self, blueprint, **options):
        """
        If the blueprint being registered if from flask, use the native
        register_blueprint function, otherwise if the Blueprint is from our
        Blueprint.py, then register the blueprint as required.
        """
        if not isinstance(blueprint, Blueprint):
            super().register_blueprint(blueprint, **options)
        else:
            # Deal with custom Blueprint objects
            blueprint.app = self
            blueprint.prepare_routes()
            blueprint.register_app(
                lambda bp: super(Flask, self).register_blueprint(bp),
                self
            )
