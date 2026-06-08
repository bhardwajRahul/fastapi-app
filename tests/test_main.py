from fastapi import FastAPI


def test_app_is_configured():
    import main

    assert isinstance(main.app, FastAPI)

    routes = {route.path for route in main.app.routes}
    assert "/api/my-model/create" in routes
    assert "/api/my-model/random" in routes
