from subprocess import STDOUT


def shell(command: str) -> str | None:
    import subprocess

    try:
        result = subprocess.check_output(command, shell=True, stderr=STDOUT).decode("utf-8").strip()
    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            f"""{command} failed.
    Exit code: {e.returncode}
    Output: {e.stdout.decode('utf-8').strip()}"""
        ) from e

    if not result:
        return None

    return result
