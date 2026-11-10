#!/usr/bin/env python3
"""Update latestversion.json for a new release.

Usage: python publish.py <version> <github-account> <platform-key>=<zip> [...]
  platform keys: win (win-x64-aot+jit), win7, linux, linux-arm64, macos-x64, macos-arm64
Example:
  python publish.py 2.2.2 myaccount win=Mesen_2.2.2_Windows.zip
Zips must be uploaded to https://github.com/<account>/MesenCE/releases/tag/<version>
under the same file name. Only the platforms you pass are replaced; others are kept.
"""
import hashlib, json, os, sys

PLATFORMS = {
    "win": ["win-x64-aot", "win-x64-jit"],
    "win7": ["win7-x64-jit"],
    "linux": ["linux-x64-aot", "linux-x64-jit"],
    "linux-arm64": ["linux-arm64-aot", "linux-arm64-jit"],
    "macos-x64": ["macos-x64-aot", "macos-x64-jit"],
    "macos-arm64": ["macos-arm64-aot", "macos-arm64-jit"],
}

def main():
    if len(sys.argv) < 4:
        sys.exit(__doc__)
    version, account = sys.argv[1], sys.argv[2]
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "latestversion.json")
    data = json.load(open(path, encoding="utf-8"))
    files = {tuple(f["Platform"]): f for f in data["Files"]}
    for arg in sys.argv[3:]:
        key, zp = arg.split("=", 1)
        h = hashlib.sha256(open(zp, "rb").read()).hexdigest().upper()
        plat = PLATFORMS[key]
        files[tuple(plat)] = {
            "Platform": plat,
            "DownloadUrl": f"https://github.com/{account}/MesenCE/releases/download/{version}/{os.path.basename(zp)}",
            "Hash": h,
        }
    data["LatestVersion"] = version
    data["Files"] = list(files.values())
    json.dump(data, open(path, "w", encoding="utf-8"), indent="\t")
    print("Updated", path)

main()
