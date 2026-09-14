from fastapi.openapi.utils import get_openapi

def custom_openapi(app):
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    public_paths = {}

    for path, path_item in openapi_schema["paths"].items():
        public_path = path

        if path.startswith("/api/auth"):
            public_path = path.replace("/api/auth", "/auth", 1)

        elif path.startswith("/api/machines"):
            public_path = path.replace("/api/machines", "/machines", 1)

        public_paths[public_path] = path_item

    openapi_schema["paths"] = public_paths

    app.openapi_schema = openapi_schema

    return app.openapi_schema
    
    
    