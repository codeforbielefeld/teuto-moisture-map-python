import nox


@nox.session(python=["3.10"])
def tests(session):
    session.install("poetry")
    session.run("poetry", "install")
    session.run("poetry", "run", "pytest")


@nox.session(python=["3.10"])
def lint(session):
    session.install("poetry")
    session.run("poetry", "install")
    session.run("poetry", "run", "black", "--check", ".")
    session.run("poetry", "run", "flake8", ".")


@nox.session(python=["3.10"])
def typing(session):
    session.install("poetry")
    session.run("poetry", "install")
    session.run("poetry", "run", "mypy", ".")
