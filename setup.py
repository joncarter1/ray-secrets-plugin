from setuptools import setup, find_packages


setup(
    name="ray-secrets",
    version="0.1",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'decrypt_ray_env_vars = ray_secrets.cli_tools:decrypt_environment_variables',
        ]
    }
)