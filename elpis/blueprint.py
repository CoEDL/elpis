from flask import Blueprint as FlaskBlueprint
from flask.blueprints import BlueprintSetupState as FlaskBlueprintSetupState
from flask.helpers import _endpoint_from_view_func


# This Blueprint implementaion extends the Flask Blueprint by allowing
# multilevel blueprints. That is Blueprints can register blueprints. This was
# does to make the server codebase modular.

# The key descision that lead to this was in understanding this code was to be
# refactored later, it would be good if endpoints for the API were as
# independent as possible (and for syntax sugar - it's cool to have
# sub-blueprints for further modularity ;) ).

# Implementing sub-blueprints introduces a few difficulties as blueprints were
# not designed to be modular. The classes below delegate the creation of
# routes to the most parent blueprint. As the most parent blueprint is being
# found, the endpoint names are generated (example "endpoints.model.new" - endpoint
# for "new" function in the "model" blueprint is contained in the "endpoints" parent
# blueprint).

# Most of the methods are overriding existing ones. See the Base classes for
# parameter and function details.


class BlueprintSetupState(FlaskBlueprintSetupState):
    """
    Overides methods to handle setting up multi-level blueprints.
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
    """
    Extend the FlaskBlueprint object to allow multi-level blueprints.
    """

    def __init__(self, name, import_name, **kwargs):
        """See flask.blueprints.Blueprint"""
        self.parent = None
        self._url_rule_queue = []
        self.blueprints = []
        self._got_registered_once = None
        super().__init__(name, import_name, **kwargs)

    def register_blueprint(self, blueprint):
        """
        Register a the given blueprint as a sub-module to this blueprint.
        Sub-module (or sub-blueprints) will have the parent paths and end points
        appended to their paths and endpoints.
        """
        # Setting the parent of a blueprint makes that a child (non-base/root)
        #   blueprint. 
        blueprint.parent = self
        self.blueprints.append(blueprint)

    def register_app(self, register, app):
        """
        From the base-blueprint, recursively add all blueprints in the
        blueprint tree (self.blueprints and their children) to the app.
        """
        if self.is_base_blueprint():
            register(self)
        else:
            self.register(app, {}, True)
        for blueprint in self.blueprints:
            blueprint.register_app(register, app)

    def register(self, app, options, first_registration=False):
        """
        Same method as flask.blueprint.Blueprint.register except slightly
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
        """
        Saves the url rule until the register function is called.
        """
        url_rule = (rule, endpoint, view_func, options)
        self._url_rule_queue.append(url_rule)

    def route(self, rule, **options):
        """
        Use the base-blueprint to route rules.
        """
        return self.route_from_base(rule, **options)

    def route_from_base(self, rule, **options):
        """
        Use the root blueprint to route a rule.
        """
        if self.is_base_blueprint():
            return super().route(rule, **options)
        return self.parent.route_from_base(rule, **options)

    def base_blueprint(self):
        """
        Recersively find the return the base blueprint.
        """
        if self.is_base_blueprint():
            return self
        return self.parent.base_blueprint()

    def get_full_endpoint(self) -> str:
        """
        Returns the full url-prefix from all blueprints up to the root parent.
        """
        if self.parent:
            # Normally having a dot('.') in the name is naughty and isn't
            # allowed because they can be accessed like attributes, but
            # for this modularity we are breaking this rule.
            return f'{self.parent.get_full_endpoint()}.{self.name}'
        else:
            return self.name

    def get_full_url_prefix(self) -> str:
        """
        Recursively build the URL prefix for this blueprint.
        """
        url_prefix = '' if self.url_prefix is None else self.url_prefix
        if self.parent:
            return f'{self.parent.get_full_url_prefix()}{url_prefix}'
        else:
            return url_prefix

    def prepare_routes(self):
        """
        Call this method to correctly setup this blueprint and the child
        blueprints before registering their rules to correct full endpoints
        and url-prefixes.
        """

        def export(new_rule, end_point, view_function, route_options):
            if self.is_base_blueprint():
                if view_function and hasattr(view_function, '__name__'):
                    assert '.' not in view_function.__name__, "Blueprint view function name should not contain dots"
                self.record(lambda s:
                            s.add_url_rule(new_rule, end_point, view_function, **route_options))
            else:
                # Remove the ability to access the vie_function like a an
                # attribute because we want a dot('.') in the endpoint name
                # for syntax sugar.
                self.record(lambda s:
                            s.add_url_rule(new_rule, end_point, view_function, **route_options))

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
        """
        Return True if this is the root blueprint.
        """
        return self.parent is None

    def __repr__(self) -> str:
        return f"{self.name}"
