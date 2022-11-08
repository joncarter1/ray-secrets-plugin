"""
Ray RuntimeEnv plugin for securely injecting secrets into the Runtime.
"""

import os
import logging

from ray._private.runtime_env.context import RuntimeEnvContext
from ray._private.runtime_env.plugin import RuntimeEnvPlugin
from ray.runtime_env import RuntimeEnv


class EnvSecretsPlugin(RuntimeEnvPlugin):
    """This plugin can be used to pass secrets to a Ray cluster using
    encrypted environment variables, preventing the actual values from
    appearing in the cluster logs.
    
    Example usage:
    ```
    runtime_env = {"secret_env_vars": {"MY_SECRET": "..ENCRYPTED_VALUE.."}}
    ```
    """

    name = "secret_env_vars"

    async def create(self, uri: str, runtime_env: RuntimeEnv, context: RuntimeEnvContext, logger: logging.Logger):
        if os.environ.get("RAY_DECRYPT_KEY") is None:
            logger.error("The environment variable RAY_DECRYPT_KEY is not set. Unable to decrypt environment variables.")
            raise ValueError
        env_vars_to_decrypt = {}
        for k,  encrypted_v in runtime_env["secret_env_vars"].items():
            env_vars_to_decrypt[f"RAY_ENCRYPTED_{k}"] = encrypted_v
        context.env_vars.update(env_vars_to_decrypt)
        context.command_prefix.append("""set -a && eval $(decrypt_ray_env_vars); set +a""")
        return