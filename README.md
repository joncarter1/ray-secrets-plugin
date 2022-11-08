# ray-secrets-plugin
A Ray RuntimeEnv plugin for securely injecting secrets at runtime.

This plugin allows environment variables to be passed to the Ray runtime through a "secret_env_vars" key, without the actual values appearing in any Ray logs.

## Example usage
See `examples/example.py`


## Notes
Contributions very welcome!

TODOs:
- Add support for asymmetric encryption
