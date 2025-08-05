# tests/conftest.py
import asyncio
import sys

import pytest

# 🔁 ¡Esto es CRÍTICO! Aplica la política ANTES de crear el loop
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


@pytest.fixture(scope="session")
def event_loop():
    """Evento personalizado para evitar el error de loop cerrado."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()
