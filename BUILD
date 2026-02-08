python_sources(
    name="lib",
    resolve=parametrize("linux", "macos"),
)

pex_binary(
    name="generate",
    entry_point="generate_qr.py",
    execution_mode="venv",
    resolve=parametrize("linux", "macos"),
)

pex_binary(
    name="detect",
    entry_point="detect_qr.py",
    execution_mode="venv",
    resolve=parametrize("linux", "macos"),
)

pex_binary(
    name="demo",
    entry_point="demo_qr.py",
    execution_mode="venv",
    resolve=parametrize("linux", "macos"),
)
