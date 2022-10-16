import nox


@nox.session(python=["3.10"])
def tests(session):
    session.run("poetry", "install", external = True)
    session.run("poetry", "run", "pytest", external= True)


@nox.session(python=["3.10"])
def lint(session):
    session.run("poetry", "install", external= True)
    session.run("poetry", "run", "black", "--check", ".", external= True)
    session.run("poetry", "run", "flake8", ".", external= True)


@nox.session(python=["3.10"])
def typing(session):
    session.run("poetry", "install", external= True)
    session.run("poetry", "run", "mypy", ".", external= True)
