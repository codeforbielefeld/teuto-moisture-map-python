import os
import sys
from tmm_api.common.auth import get_digest


def main():
    if not os.getenv("TMM_AUTH_SECRET"):
        print("Error: TMM_AUTH_SECRET environment variable is not set", file=sys.stderr)
        sys.exit(1)

    if len(sys.argv) != 2:
        print("Usage: uv run scripts/keygen.py <device-id>", file=sys.stderr)
        print("Example: uv run scripts/keygen.py 'eui-07dfg8okhjdsf98g7zk'", file=sys.stderr)
        sys.exit(1)

    device_id = sys.argv[1]

    if not device_id.islower():
        print(
            "Warning: Device ID is not in lower case, are you sure the device id is in the format send by the device?",
            file=sys.stderr,
        )
    if not device_id.startswith("eui-"):
        print(
            "Warning: Device ID should usually start with 'eui-' did you forget to use the correct format?",
            file=sys.stderr,
        )

    try:
        api_key = get_digest(device_id)
        print(f"Device ID: {device_id}")
        print(f"TMM-APIKEY: {api_key}")
    except Exception as e:
        print(f"Error generating digest: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
