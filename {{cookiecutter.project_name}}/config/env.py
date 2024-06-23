from pathlib import Path

import environ

env = environ.Env()

# Project base directory
BASE_DIR = Path(__file__).parent.parent

# Set default values for environment variables if they are not set
env.read_env(BASE_DIR / ".env")


def get_env_value(env_variable: str, cast: type, default: str = None):
    """Get a value from the environment and cast it to the specified type."""
    return env(env_variable, cast, default)
