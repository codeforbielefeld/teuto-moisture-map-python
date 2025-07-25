FROM python:3.13-alpine as base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

WORKDIR /app

FROM base as builder

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

# Install uv
RUN pip install uv
RUN python -m venv /venv

# TODO: Install dependencies in a single layer again
# COPY pyproject.toml uv.lock ./
# RUN uv export --no-hashes --format requirements-txt | /venv/bin/pip install -r /dev/stdin

COPY . .
RUN uv build --wheel && /venv/bin/pip install dist/*.whl

FROM base as final

COPY --from=builder /venv /venv
ENV PATH="/venv/bin:${PATH}" \
    VIRTUAL_ENV="/venv"

#CMD ["flask","--app=ttn_hook:app",  "run", "--host=0.0.0.0"]
ENTRYPOINT [ "uvicorn", "--host", "0.0.0.0", "--port", "5000", "tmm_api:app"]