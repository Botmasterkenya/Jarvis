import json
import subprocess
import webbrowser
import psutil

def execute(response_text: str) -> dict:
    """
    Look at what Gemini responded.
    If it's a JSON action → run it on the system.
    If it's normal text  → just return it to be spoken.
    """
    text = response_text.strip()

    if text.startswith('{'):
        try:
            data   = json.loads(text)
            action = data.get("action", "")
            spoken = data.get("speak", "Done.")
            result = _run_action(action, data)
            return {
                "type":   "action",
                "action": action,
                "spoken": spoken,
                "result": result,
                "raw":    text
            }
        except json.JSONDecodeError:
            pass

    # Plain conversation response
    return {
        "type":   "text",
        "spoken": text,
        "result": None,
        "raw":    text
    }

def _run_action(action: str, data: dict) -> str:
    if action == "run_command":
        return _run_command(data.get("command", ""))

    elif action == "open_app":
        app = data.get("app", "")
        subprocess.Popen(
            [app],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return f"Opened {app}"

    elif action == "open_url":
        url = data.get("url", "")
        webbrowser.open(url)
        return f"Opened {url}"

    elif action == "system_info":
        return _get_system_info()

    return "Unknown action."

def _run_command(cmd: str) -> str:
    try:
        out = subprocess.check_output(
            cmd, shell=True,
            stderr=subprocess.STDOUT,
            timeout=15, text=True
        )
        return out.strip() or "Command ran successfully."
    except subprocess.CalledProcessError as e:
        return f"Error: {e.output.strip()}"
    except subprocess.TimeoutExpired:
        return "Command timed out."

def _get_system_info() -> str:
    cpu  = psutil.cpu_percent(interval=1)
    ram  = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    return (
        f"CPU: {cpu}% | "
        f"RAM: {ram.used // 1024 // 1024}MB "
        f"of {ram.total // 1024 // 1024}MB ({ram.percent}%) | "
        f"Disk: {disk.used // 1024 // 1024 // 1024}GB "
        f"of {disk.total // 1024 // 1024 // 1024}GB"
    )

def get_system_stats() -> dict:
    """Returns raw numbers for the web dashboard gauges."""
    ram  = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    return {
        "cpu":         psutil.cpu_percent(interval=0.5),
        "ram_percent": ram.percent,
        "ram_used":    ram.used  // 1024 // 1024,
        "ram_total":   ram.total // 1024 // 1024,
        "disk_used":   disk.used  // 1024 // 1024 // 1024,
        "disk_total":  disk.total // 1024 // 1024 // 1024,
    }