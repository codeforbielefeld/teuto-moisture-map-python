import nox

nox.options.sessions = ["tests", "lint", "typing"]


@nox.session(python=False)
def tests(session):
    session.run("poetry", "install", external=True)
    session.run("poetry", "run", "pytest", external=True)


@nox.session(python=False)
def lint(session):
    session.run("poetry", "install", external=True)
    session.run("poetry", "run", "black", "--check", ".", external=True)
    session.run("poetry", "run", "ruff", ".", external=True)


@nox.session(python=False)
def typing(session):
    session.run("poetry", "install", external=True)
    session.run("poetry", "run", "mypy", ".", external=True)


@nox.session(python=False)
def serv(session):
    session.run("poetry", "install", external=True)
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
            "INFLUX_CONFIG_FILE": "../../examples/influx_config.local.ini",
            "TMM_BUCKET": "tmm-bucket",
        },
    )
