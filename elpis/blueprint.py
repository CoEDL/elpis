from flask import Blueprint as FlaskBlueprint

class Blueprint(FlaskBlueprint):
    """ Extend the FlaskBlueprint object to allow sub blueprints
    via the `parent` keyword argument.
    """
    def __init__(self, name, import_name, **kwargs):
        print(f'@ __init__(name={name}, import_name={import_name}, ...)')
        self.parent = None
        self._url_rule_queue = []
        super().__init__(name, import_name, **kwargs)
    
    def register_blueprint(self, blueprint):
        print(f'@ register_blueprint(blueprint={blueprint})')
        self.parent = blueprint
        print(f'! queue: {self._url_rule_queue}')

    def add_url_rule(self, rule, endpoint=None, view_func=None, **options):
        """Like :meth:`Flask.add_url_rule` but for a blueprint.  The endpoint for
        the :func:`url_for` function is prefixed with the name of the blueprint.
        """
        print(f'@ add_url_rule(rule={rule},endpoint={endpoint},view_func={view_func})')
        url_rule = (rule, endpoint, view_func, options)
        self._url_rule_queue.append(url_rule)
        # if self.is_base_blueprint():
        #     if view_func and hasattr(view_func, '__name__'):
        #         assert '.' not in view_func.__name__, "Blueprint view function name should not contain dots"
        #     self.record(lambda s:
        #         s.add_url_rule(rule, endpoint, view_func, **options))
        # else:
        #     self._registeration_queue.append(lambda s:
        #         s.add_url_rule(rule, endpoint, view_func, **options))
        # print(f'! What is my endpoint for {rule}? -> {endpoint}')
        # if self.parent is not None:
        #     rule = self.parent.rule + rule
        #     endpoint = self.get_endpoint()
        #     print(f'! I think it is {rule}? -> {endpoint}')
        #     self.record(lambda s:
        #         s.add_url_rule(rule, endpoint, view_func, **options))
        # else:
        #     print('! using old func')
        #     if view_func and hasattr(view_func, '__name__'):
        #         assert '.' not in view_func.__name__, "Blueprint view function name should not contain dots"
        #     self.record(lambda s:
        #         s.add_url_rule(rule, endpoint, view_func, **options))

    def route(self, rule, **options):
        print(f'@ route(rule={rule})')
        return self.route_from_base(rule, **options)
        # url_prefix = ''
        # if self.url_prefix:
        #     url_prefix += self.url_prefix
        # if self.parent:
        #     return self.parent.route(url_prefix + rule, **options)
        # else:
        #     return super().route(rule, **options)
    
    def route_from_base(self, rule, **options):
        if self.is_base_blueprint():
            return super().route(rule, **options)
        return self.parent.route_from_base(rule, **options)
    
    def get_full_endpoint(self) -> str:
        if self.parent:
            return f'{self.parent.get_full_endpoint()}.{self.name}'
        else:
            return self.name
    
    def prepare_routes(self):
        if self.is_base_blueprint():
            for url_rule in self._url_rule_queue:
                rule, endpoint, view_func, options = url_rule
                if view_func and hasattr(view_func, '__name__'):
                    assert '.' not in view_func.__name__, "Blueprint view function name should not contain dots"
                self.record(lambda s:
                    s.add_url_rule(rule, endpoint, view_func, **options))

    def is_base_blueprint(self) -> bool:
        return self.parent is None

    def __repr__(self) -> str:
        return f"{self.name}"

        
        