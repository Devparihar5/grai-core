import typer
import os
from confuse import LazyConfig, YamlSource, CONFIG_FILENAME

from confuse import OneOf, MappingValues, Optional, Choice


class ConfuseParameters:
    def __init__(self, template, default_values, redacted_fields):
        self.template = template
        self.default_values = default_values
        self.redacted_fields = redacted_fields


def apply_redactions(config_to_redact: LazyConfig, redact_dict: dict):
    for path, value in redact_dict.items():
        view = config_to_redact
        for key in path.split('.'):
            view = view[key]
        view.redact = value


class GraiLazyConfig(LazyConfig):
    def __init__(self, name: str, parameters: ConfuseParameters):
        super().__init__(name, __name__)

        self.parameters = parameters
        self.set_env()
        self.set_args(self.parameters.default_values, dots=True)
        apply_redactions(self, self.parameters.redacted_fields)


    @property
    def config_filename(self):
        return os.path.join(self.config_dir(), CONFIG_FILENAME)

    def view(self):
        typer.echo(f"\nfile: {self.config_filename}")
        typer.echo("\n-------------------------------\n")
        typer.echo(self.dump(self.parameters.template, redact=True))

    def grab(self, value: str):
        base = self.get(self.parameters.template)
        for key in value.split('.'):
            base = base[key]
        return base


def _get_config_template():
    ##########################

    api_versions = Choice(choices={'v1'})
    server_template = {
        "host": str,
        "port": str,
        "api_version": Optional(api_versions, default='v1', allow_missing=True)
    }

    ##########################
    auth_modes = Choice(choices={'username', 'api'})
    auth_typer = lambda default: Optional(auth_modes, default=default, allow_missing=True)

    auth_user_template = {
        "username": str,
        "password": str,
        "authentication_mode": Optional(auth_modes, default='username', allow_missing=True),
    }

    auth_api_template = {
        "api_key": str,
        "authentication_mode": Optional(auth_modes, default='api', allow_missing=True),
    }

    auth_template = OneOf([auth_user_template, auth_api_template])

    ###########################

    context_template = {
        "namespace": str
    }

    ###########################

    template = {
        "server": server_template,
        "auth": auth_template,
        "context": context_template,
    }
    return template


def get_config_parameters():
    default_values = {
        "server.host": "localhost",
        "server.port": "8000",
        "context.namespace": "default",
    }

    redacted_fields = {
        'auth.password': True,
        'auth.api_key': True,
    }

    template = _get_config_template()

    return ConfuseParameters(template, default_values, redacted_fields)


config = GraiLazyConfig('grai', get_config_parameters())
