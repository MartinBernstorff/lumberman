from subprocess import STDOUT
from typing import Optional


def interactive_cmd(command: str) -> None:
    import subprocess

    try:
        subprocess.run(command, shell=True, stderr=STDOUT, check=True)
    except subprocess.CalledProcessError as e:
        error_message = f"""{command} failed.
\tExit code: {e.returncode}"""

        if e.stdout:
            error_message += f"\n\tOutput: {e.stdout.decode('utf-8').strip()}"

        raise RuntimeError(error_message) from e


def shell_output(command: str) -> Optional[str]:
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
