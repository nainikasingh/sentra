import subprocess

def check_port_open(port: int) -> str:
    """
    Check if a specific port is open on localhost.

    Args:
        port (int): The port number to check.

    Returns:
        str: A message indicating whether the port is open or closed.
    """
    try:
        result = subprocess.run(
            ["nc", "-z", "localhost", str(port)],
            capture_output=True,
            text=True,
            timeout=5
        )
        return f"Port {port} is open" if result.returncode == 0 else f"Port {port} is closed"
    except Exception as e:
        return f"Error checking port: {e}"