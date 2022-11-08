import os
import re

from ray_secrets.encrypt import decrypt_secret


def decrypt_environment_variables():
    """Decrypts environment variables that have the suffix "RAY_ENCRYPTED_", printing out the unencrypted versions.

    Env variables are decrypted with RAY_DECRYPT_KEY. (Currently a symmetric Fernet key, TODO: Assymmetric support)

    Example usage (after setting encrypted environment variables):
    ```
    > decrypt_env_vars
    SECRET=..UNENCRYPTED_VALUE..
    ```
    This is used by the EnvSecretsPlugin to set environment variables from encrypted values by running:
    `set -a && eval $(decrypt_env_vars); set +a`
    """
    if (decrypt_key := os.environ.get("RAY_DECRYPT_KEY")) is None:
        raise ValueError("Failed to find a Ray decryption key. Unable to decrypt env vars.")

    decrypted_env_vars = ""
    for key, encrypted_value in os.environ.items():
        regex_match = re.search("RAY_ENCRYPTED_(.+)", key)
        if regex_match is None:
            continue
        env_var_name = regex_match.group(1)
        decrypted_env_vars += f"{env_var_name}={decrypt_secret(encrypted_value, key=decrypt_key)}\n"
    print(decrypted_env_vars)