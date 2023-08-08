import nox

nox.options.sessions = ["test", "black", "ruff", "typing"]


@nox.session(python=False)
def test(session):
    session.run("poetry", "install", "--quiet", external=True)
    session.run("poetry", "run", "pytest", external=True)


@nox.session(python=False)
def black(session):
    session.run("poetry", "install", "--quiet", external=True)
    session.run("poetry", "run", "black", "--check", ".", external=True)


@nox.session(python=False)
def ruff(session):
    session.run("poetry", "install", "--quiet", external=True)
    session.run("poetry", "run", "ruff", ".", external=True)


@nox.session(python=False)
def typing(session):
    session.run("poetry", "install", "--quiet", external=True)
    session.run("poetry", "run", "mypy", ".", external=True)


@nox.session(python=False)
def serv(session):
    session.run("poetry", "install", "--quiet", external=True)
    session.run(
        "poetry",
        "run",
        "uvicorn",
        "--host",
        "0.0.0.0",
        "--port",
        "5000",
        "--reload",
        "--reload-include",
        "*.flux",
        "tmm_api:app",
        external=True,
        env={
            "DEVELOPMENT_MODE": "true",
            "ENABLE_WRITE": "true",
            "TMM_AUTH_SECRET": "secret",
            "INFLUX_CONFIG_FILE": "influx_config.local.ini",
            "TMM_BUCKET": "tmm-bucket",
        },
    )
