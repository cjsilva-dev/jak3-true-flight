"""Add the latest release of this repo to mod-source.json (the OpenGOAL launcher mod source).

Run by .github/workflows/update-mod-source.yml after a successful "Cut Mod Release".
Only adds the version once all three downloads answer, and never twice."""
import json, os, sys, urllib.request

repo = os.environ["GITHUB_REPOSITORY"]             # e.g. cjsilva-dev/jak3-true-flight
mod_key = os.environ.get("MOD_KEY", "true-flight")  # entry in mod-source.json
game = os.environ.get("MOD_GAME", "jak3")
token = os.environ["GITHUB_TOKEN"]

req = urllib.request.Request(f"https://api.github.com/repos/{repo}/releases/latest",
                             headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"})
rel = json.load(urllib.request.urlopen(req))
tag = rel["tag_name"]                     # v0.1.1
version = tag.lstrip("v")
names = {a["name"] for a in rel["assets"]}
assets = {"windows": f"windows-{tag}.zip", "linux": f"linux-{tag}.tar.gz", "macos": f"macos-intel-{tag}.tar.gz"}
missing = [f for f in assets.values() if f not in names]
if missing:
    sys.exit(f"release {tag} is missing {missing}; not updating")

path = "mod-source.json"
src = json.load(open(path))
mod = src["mods"][mod_key]
if any(v["version"] == version for v in mod["versions"]):
    print(f"{version} already listed"); sys.exit(0)

base = f"https://github.com/{repo}/releases/download/{tag}/"
entry = {
    "version": version,
    "publishedDate": rel["published_at"],
    "supportedGames": [game],
    "settings": {"decompConfigOverride": "", "shareVanillaSaves": False},
    "assets": {k: base + v for k, v in assets.items()},
    "assetDownloadCounts": {"windows": 0, "linux": 0, "macos": 0},
}
mod["versions"].insert(0, entry)          # newest first
src["lastUpdated"] = rel["published_at"]
open(path, "w").write(json.dumps(src, indent=2) + "\n")
print(f"added {mod_key} {version}")
