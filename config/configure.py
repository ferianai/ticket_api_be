import os


def configure_app(var_name):
    variable_value = os.getenv(var_name)
    if variable_value is None:
        raise ValueError(f"Environment variable '{var_name}' is not set.")
    return variable_value


DB_USER = configure_app("DB_USER")
DB_PASSWORD = configure_app("DB_PASSWORD")
DB_HOST = configure_app("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT", 5432))  # Default to 5432 if not set
DB_NAME = configure_app("DB_NAME")
SQLALCHEMY_DATABASE_URI = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


JWT_SECRET_KEY = configure_app("JWT_SECRET_KEY")
JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", 3600))
JWT_REFRESH_TOKEN_EXPIRES = int(os.getenv("JWT_REFRESH_TOKEN_EXPIRES", 604800))
