# ---------- builder ----------
FROM python:3.11-slim AS builder
WORKDIR /build

RUN apt-get update && apt-get install -y git build-essential && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md ./
COPY . .

RUN pip install --upgrade pip build hatchling

# Build wheel
RUN python -m build --wheel --outdir /build/dist

# ---------- runtime ----------
FROM python:3.11-slim
WORKDIR /app

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Copy wheel from builder and install
COPY --from=builder /build/dist/*.whl /tmp/
RUN pip install --upgrade pip && pip install /tmp/*.whl && rm -rf /tmp/*.whl

# Optional: copy entrypoint code if needed
COPY src/reposage ./reposage

ENTRYPOINT ["python", "-m", "reposage.main"]