from flask import Blueprint as FlaskBlueprint
from flask.blueprints import BlueprintSetupState as FlaskBlueprintSetupState


class BlueprintSetupState(FlaskBlueprintSetupState):
    """Overrided methods to handle setting up multi-level blueprints.
    See flask.blueprints.BlueprintSetupState for purpose.
    """

    def add_url_rule(self, rule, endpoint=None, view_func=None, **options):
        if self.url_prefix is not None:
            if rule:
                rule = f'{self.blueprint.get_full_url_prefix()}{rule}'
            else:
                rule = self.url_prefix
        options.setdefault('subdomain', self.subdomain)
        if endpoint is None:
            endpoint = _endpoint_from_view_func(view_func)
        else:
            endpoint = f'{self.blueprint.get_full_endpoint()}.{endpoint}'
        defaults = self.url_defaults
        if 'defaults' in options:
            defaults = dict(defaults, **options.pop('defaults'))
        self.app.add_url_rule(rule, endpoint, view_func, defaults=defaults, **options)


class Blueprint(FlaskBlueprint):
    """ Extend the FlaskBlueprint object to allow multi-level blueprints.
    """
    def __init__(self, name, import_name, **kwargs):
        """See flask.blueprints.Blueprint"""
        self.parent = None
        self._url_rule_queue = []
        self.blueprints = []
        super().__init__(name, import_name, **kwargs)
    
    def register_blueprint(self, blueprint):
        """ Register a the given blueprint as a sub-module to this blueprint.
        Sub-module (or sub-blueprints) will have the parent paths and end points
        appended to their paths and endpoints.
        """
        # Setting the parent of a blueprint makes that a child (non-base/root)
        #   blueprint. 
        blueprint.parent = self
        self.blueprints.append(blueprint)
    
    def register_app(self, register, app):
        """From the base-blueprint, recursively add all blueprints in the
        blueprint tree (self.blueprints and their children) to the app.
        """
        if self.is_base_blueprint():
            register(self)
        else:
            self.register(app, {}, True)
        for blueprint in self.blueprints:
            blueprint.register_app(register, app)
    
    def register(self, app, options, first_registration=False):
        """Same method as flask.blueprint.Blueprint.register except slightly
        modified to handle multi-level blueprints.
        """
        self._got_registered_once = True
        state = BlueprintSetupState(self, app, options, first_registration)

        if self.has_static_folder:
            state.add_url_rule(
                self.static_url_path + '/<path:filename>',
                view_func=self.send_static_file, endpoint='static'
            )

        for deferred in self.deferred_functions:
            deferred(state)

    def add_url_rule(self, rule, endpoint=None, view_func=None, **options):
        """Saves the url rule until the register function is called.
        """
        url_rule = (rule, endpoint, view_func, options)
        self._url_rule_queue.append(url_rule)

    def route(self, rule, **options):
        """Use the base-blueprint to route rules."""
        return self.route_from_base(rule, **options)
    
    def route_from_base(self, rule, **options):
        if self.is_base_blueprint():
            return super().route(rule, **options)
        return self.parent.route_from_base(rule, **options)

    def base_blueprint(self):
        if self.is_base_blueprint():
            return self
        return self.parent.base_blueprint()
    
    def get_full_endpoint(self) -> str:
        """Returns the full url-prefix from all blueprints up to the root parent.
        """
        if self.parent:
            return f'{self.parent.get_full_endpoint()}.{self.name}'
        else:
            return self.name

    def get_full_url_prefix(self) -> str:
        url_prefix = '' if self.url_prefix is None else self.url_prefix
        if self.parent:
            return f'{self.parent.get_full_url_prefix()}{url_prefix}'
        else:
            return url_prefix
    
    
    def prepare_routes(self):
        """Call this method to correctly setup this blueprint and the child
        blueprints before registering their rules to correct full endpoints
        and url-prefixes.
        """
        def export(rule, endpoint, view_func, options):
            if self.is_base_blueprint():
                if view_func and hasattr(view_func, '__name__'):
                    assert '.' not in view_func.__name__, "Blueprint view function name should not contain dots"
                self.record(lambda s:
                    s.add_url_rule(rule, endpoint, view_func, **options))
            else:
                self.record(lambda s:
                    s.add_url_rule(rule, endpoint, view_func, **options))

        # prepare child routes now
        for blueprint in self.blueprints:
            blueprint.prepare_routes()

        # prepare this blueprints routes here
        if self.is_base_blueprint():
            for url_rule in self._url_rule_queue:
                export(*url_rule)
        else:
            for url_rule in self._url_rule_queue:
                rule, endpoint, view_func, options = url_rule
                export(rule, endpoint, view_func, options)

    def is_base_blueprint(self) -> bool:
        """Return True if this is the root blueprint."""
        return self.parent is None

    def __repr__(self) -> str:
        return f"{self.name}"

        
        