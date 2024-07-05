from pathlib import Path

import requests


def download_to_local(url: str, out_path: Path, parent_mkdir: bool = True) -> bool:
    if not isinstance(out_path, Path):
        raise ValueError(f"{out_path} must be a valid Path object")
    if parent_mkdir:
        out_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        # write the file out in binary
        # mode to prevent any newlines conversions
        out_path.write_bytes(response.content)
        return True
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {url} due to {e}")
        return False
