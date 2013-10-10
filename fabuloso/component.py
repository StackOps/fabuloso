#!/usr/bin/python
#   Copyright 2012-2013 STACKOPS TECHNOLOGIES S.L.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
import inspect


class Component(object):

    # List of attributes obtained at definition time, when
    # the 'fabuloso' entity reads from component.yml
    _services = {}
    _module = None
    _name = None
    _provider = None

    # List of attributes obtained at execution time, when the
    # user decides where to run this component and its properties
    _properties = {}

    """Parses component files and extracts its data"""
    def __init__(self, name, module, services, provider):
        self._name = name
        self._module = module
        self._services = services
        self._provider = provider
        self._set_attributes()

    def set_environment(self, env):
        self._provider.set_environment(env)

    def set_properties(self, props):
        self._properties = props

    def get_properties(self):
        return self._properties

    def _set_attributes(self):
        """ Set the dynamically set services. """
        for service in self._services.keys():
            setattr(self, service, self._define_service(service))

    def execute_service(self, service_name):
        """ Indirect way to execute service.

        Although you can execute the dynamically-inserted services in a
        component via component.service_name(), you might want to execute
        them this way.
        """
        getattr(self, service_name)()

    def _define_service(self, service_name):
        """ Return the function that will execute the service.

        This method is used to insert in the component the function
        that will execute a service.
        """
        def wrapper_method():
            description, methods = self._services[service_name]
            for method in methods:
                service_args = self._build_args(method)
                self._provider.execute_method(getattr(self._module, method),
                                              **service_args)

        return wrapper_method

    def _build_args(self, method):
        """ Build appropiate args depending on the method

        The execute service receives a list of arguments that may be
        useful for one or more methods. This function filters only
        the ones that are needed for the current 'method'
        """
        method_args = {}
        parameters = self._get_method_params(method)
        for parameter in parameters:
            if parameter in self._properties:
                method_args[parameter] = self._properties[parameter]
        return method_args

    def _get_method_params(self, method):
        """ Get method parameters.

        Use introspection to retrieve the list of parameters that
        a method needs
        """
        meth = getattr(self._module, method)
        return inspect.getargspec(meth).args

    def _get_param_default(self, param, method):
        """ Get the default value of a parameter
        """
        meth = getattr(self._module, method)
        args = inspect.getargspec(meth).args

        defaults = inspect.getargspec(meth).defaults
        if defaults is not None:

            # only the n-last arguments have default arguments, where
            # n == the lenght of defaults
            args = args[len(args) - len(defaults):]
            if param in args:
                index = args.index(param)
                default_value = defaults[index]
                return default_value

        return ""

    def __repr__(self):
        return '<Component {} at {}>'.format(self._name, self._module)

    def to_dict(self):
        return {
            'name': self._name
        }
