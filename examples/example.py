"""
Example of securely injecting secrets into the Ray runtime.
In practice, encryption and decryption keys can be issued by a secrets engine such as Vault:
https://www.vaultproject.io/
"""
import os
import ray
from ray_secrets import encrypt_secret, keygen

def main():
    # Setting up encryption plugin
    encryption_key = decryption_key = keygen()
    os.environ["RAY_ENCRYPT_KEY"] = encryption_key
    os.environ["RAY_DECRYPT_KEY"] = decryption_key
    os.environ["RAY_RUNTIME_ENV_PLUGINS"] = """[{"class": "ray_secrets.plugin.EnvSecretsPlugin"}]"""

    my_secret = "foo"
    my_encrypted_secret = encrypt_secret(my_secret)
    runtime_env = {"pip": ["cryptography"], "secret_env_vars": {"MY_SECRET": my_encrypted_secret}}
    
    @ray.remote
    def test_func(secret_val):
        env_secret = os.environ.get("MY_SECRET")
        print(f"Env secret={env_secret}. Passed secret={secret_val}.")
        return secret_val == env_secret

    ray.init(runtime_env=runtime_env)
    out = test_func.remote(my_secret)
    result = ray.get(out)
    if result:
        print("Success!")


if __name__ == "__main__":
    main()