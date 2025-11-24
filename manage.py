#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import socket

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CocosBurger.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    if 'runserver' in sys.argv and os.environ.get('RUN_MAIN') == 'true':
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            print(f"----------------------------------------------------------")
            print(f"  LAN: http://{ip}:8000")
            print(f"----------------------------------------------------------")
            print(f"  Local: http://127.0.0.1:8000")
            print(f"----------------------------------------------------------")
        except Exception:
            pass

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
