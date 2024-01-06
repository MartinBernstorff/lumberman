def run_command(command: str) -> str | None:
    import subprocess

    result = (
        subprocess.check_output(command, shell=True)
        .decode("utf-8")
        .strip()
    )

    if not result:
        return None

    return result
