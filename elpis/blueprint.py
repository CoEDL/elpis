from flask import Blueprint as FlaskBlueprint

class BlueprintSetupState(object):
    """Temporary holder object for registering a blueprint with the
    application.  An instance of this class is created by the
    :meth:`~flask.Blueprint.make_setup_state` method and later passed
    to all register callback functions.
    """

    def __init__(self, blueprint, app, options, first_registration):
        #: a reference to the current application
        self.app = app

        #: a reference to the blueprint that created this setup state.
        self.blueprint = blueprint

        #: a dictionary with all options that were passed to the
        #: :meth:`~flask.Flask.register_blueprint` method.
        self.options = options

        #: as blueprints can be registered multiple times with the
        #: application and not everything wants to be registered
        #: multiple times on it, this attribute can be used to figure
        #: out if the blueprint was registered in the past already.
        self.first_registration = first_registration

        subdomain = self.options.get('subdomain')
        if subdomain is None:
            subdomain = self.blueprint.subdomain

        #: The subdomain that the blueprint should be active for, ``None``
        #: otherwise.
        self.subdomain = subdomain

        url_prefix = self.options.get('url_prefix')
        if url_prefix is None:
            url_prefix = self.blueprint.url_prefix
        #: The prefix that should be used for all URLs defined on the
        #: blueprint.
        self.url_prefix = url_prefix

        #: A dictionary with URL defaults that is added to each and every
        #: URL that was defined with the blueprint.
        self.url_defaults = dict(self.blueprint.url_values_defaults)
        self.url_defaults.update(self.options.get('url_defaults', ()))

    def add_url_rule(self, rule, endpoint=None, view_func=None, **options):
        """A helper method to register a rule (and optionally a view function)
        to the application.  The endpoint is automatically prefixed with the
        blueprint's name.
        """
        if self.url_prefix is not None:
            if rule:
                rule = f'{self.blueprint.get_full_url_prefix()}{rule}'
            else:
                rule = self.url_prefix
        options.setdefault('subdomain', self.subdomain)
        if endpoint is None:
            endpoint = _endpoint_from_view_func(view_func)
        else:
            print(f'! endpoint prefix: {self.blueprint.get_full_endpoint()}')
            endpoint = f'{self.blueprint.get_full_endpoint()}.{endpoint}'
        defaults = self.url_defaults
        if 'defaults' in options:
            defaults = dict(defaults, **options.pop('defaults'))
        self.app.add_url_rule(rule, endpoint, view_func, defaults=defaults, **options)

class Blueprint(FlaskBlueprint):
    """ Extend the FlaskBlueprint object to allow sub blueprints
    via the `parent` keyword argument.
    """
    def __init__(self, name, import_name, **kwargs):
        print(f'@ __init__(name={name}, import_name={import_name}, ...)')
        self.parent = None
        self.app = None
        self._url_rule_queue = []
        self.blueprints = []
        super().__init__(name, import_name, **kwargs)
    
    def register_blueprint(self, blueprint):
        print(f'@ register_blueprint(blueprint={blueprint})')
        blueprint.parent = self
        self.blueprints.append(blueprint)
        print(f'! queue: {self._url_rule_queue}')
        print(f'! queue: {self.blueprints}')
    
    def register_app(self, register, app):
        if self.is_base_blueprint():
            register(self)
        else:
            self.register(app, {}, True)
        for blueprint in self.blueprints:
            blueprint.register_app(register, app)
    
    def register(self, app, options, first_registration=False):
        """Called by :meth:`Flask.register_blueprint` to register all views
        and callbacks registered on the blueprint with the application. Creates
        a :class:`.BlueprintSetupState` and calls each :meth:`record` callback
        with it.

        :param app: The application this blueprint is being registered with.
        :param options: Keyword arguments forwarded from
            :meth:`~Flask.register_blueprint`.
        :param first_registration: Whether this is the first time this
            blueprint has been registered on the application.
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
        """Like :meth:`Flask.add_url_rule` but for a blueprint.  The endpoint for
        the :func:`url_for` function is prefixed with the name of the blueprint.
        """
        print(f'@ add_url_rule(rule={rule},endpoint={endpoint},view_func={view_func})')
        url_rule = (rule, endpoint, view_func, options)
        self._url_rule_queue.append(url_rule)

    def route(self, rule, **options):
        print(f'@ route(rule={rule})')
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
        app = self.base_blueprint().app
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

        # prepare my routes here
        print('@ prepare_routes')
        
        if self.is_base_blueprint():
            print(f'! exporting base url rules: {self._url_rule_queue}')
            for url_rule in self._url_rule_queue:
                export(*url_rule)
        else:
            print(f'! exporting non-base url rules: {self._url_rule_queue}')
            for url_rule in self._url_rule_queue:
                rule, endpoint, view_func, options = url_rule
                export(rule, endpoint, view_func, options)



    def is_base_blueprint(self) -> bool:
        return self.parent is None

    def __repr__(self) -> str:
        return f"{self.name}"

        
        