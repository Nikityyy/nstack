"""Link nstack from this checkout into the selected provider profiles."""

import argparse
import os
from pathlib import Path
import shutil
import stat
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
RULES = ROOT / "rules" / "nstack.md"
START = "<!-- nstack:start -->"
END = "<!-- nstack:end -->"
WINDOWS_JUNCTION = getattr(stat, "IO_REPARSE_TAG_MOUNT_POINT", -1)


def link_target(path):
    if not os.path.lexists(path):
        return None, False
    info = path.lstat()
    junction = getattr(info, "st_reparse_tag", 0) == WINDOWS_JUNCTION
    if stat.S_ISLNK(info.st_mode) or junction:
        target = os.readlink(path)
        if os.name == "nt" and target.startswith("\\\\?\\UNC\\"):
            target = "\\\\" + target[8:]
        elif os.name == "nt" and target.startswith("\\\\?\\"):
            target = target[4:]
        return (path.parent / target).resolve(), junction
    return None, False


def create_link(path, source):
    if os.name != "nt":
        path.symlink_to(source, target_is_directory=True)
        return
    subprocess.run(
        [
            "powershell.exe", "-NoProfile", "-NonInteractive", "-Command",
            "$ErrorActionPreference = 'Stop'; "
            "$source = [WildcardPattern]::Escape($env:NSTACK_SOURCE); "
            "New-Item -ItemType Junction -Path $env:NSTACK_LINK "
            "-Target $source | Out-Null",
        ],
        env={**os.environ, "NSTACK_LINK": str(path), "NSTACK_SOURCE": str(source)},
        check=True,
    )


def skill_changes(folder, sources):
    add = []
    remove = []
    for name, source in sources.items():
        destination = folder / name
        target, _ = link_target(destination)
        if target == source:
            continue
        if os.path.lexists(destination):
            raise ValueError(f"Existing entry at {destination}. Move it aside or choose another profile.")
        add.append((destination, source))

    if folder.is_dir():
        for path in folder.iterdir():
            if path.name in sources:
                continue
            target, junction = link_target(path)
            if target and target.parent == SKILLS and target.name == path.name:
                remove.append((path, junction))
    return add, remove


def rule_contents(path):
    current = path.read_bytes().decode("utf-8") if path.exists() else ""
    newline = "\r\n" if "\r\n" in current else "\n"
    block = newline.join((
        START,
        f"Read and follow the nstack working rules at `{RULES.as_posix()}` when starting a task.",
        END,
    ))
    if START in current or END in current:
        if current.count(START) != 1 or current.count(END) != 1 or current.index(START) > current.index(END):
            raise ValueError(f"Unmatched or repeated nstack markers in {path}.")
        before, _, rest = current.partition(START)
        _, _, after = rest.partition(END)
        new = before + block + after
    else:
        separator = ("" if not current else newline if current.endswith("\n") else newline * 2)
        new = current + separator + block + newline
    return new.encode("utf-8") if new != current else None


def write_rules(path, contents):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as file:
        temporary = Path(file.name)
    try:
        temporary.write_bytes(contents)
        if path.exists():
            shutil.copymode(path, temporary)
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codex", type=Path, action="append", default=[], metavar="HOME",
                        help="Codex home, such as ~/.codex. May be repeated.")
    parser.add_argument("--claude", type=Path, action="append", default=[], metavar="HOME",
                        help="Claude config directory, such as ~/.claude. May be repeated.")
    parser.add_argument("--skills-dir", type=Path, action="append", default=[], metavar="DIR",
                        help="Local skill directory for another provider. May be repeated.")
    parser.add_argument("--rules-file", type=Path, action="append", default=[], metavar="FILE",
                        help="An existing provider's global instructions file. May be repeated.")
    args = parser.parse_args()

    profiles = [(home, "AGENTS.md") for home in args.codex]
    profiles.extend((home, "CLAUDE.md") for home in args.claude)
    folders = {path.expanduser().resolve() for path in args.skills_dir}
    rule_files = {path.expanduser().resolve() for path in args.rules_file}
    for home, rule_name in profiles:
        root = home.expanduser().resolve()
        folders.add((root / "skills").resolve())
        rule_files.add((root / rule_name).resolve())
    if not folders and not rule_files:
        parser.error("choose at least one profile or destination")

    try:
        sources = {path.name: path.resolve() for path in SKILLS.iterdir() if (path / "SKILL.md").is_file()}
        if not sources or not RULES.is_file():
            raise ValueError(f"Incomplete nstack checkout at {ROOT}.")
        changes = {folder: skill_changes(folder, sources) for folder in sorted(folders)}
        rules = {path: rule_contents(path) for path in sorted(rule_files)}

        for folder, (add, remove) in changes.items():
            folder.mkdir(parents=True, exist_ok=True)
            for path, source in add:
                create_link(path, source)
            for path, junction in remove:
                (path.rmdir if junction else path.unlink)()
            print(f"Skills ready at {folder}")
        for path, contents in rules.items():
            if contents is not None:
                write_rules(path, contents)
            print(f"Working rules referenced from {path}")
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"nstack: {error}\n")


if __name__ == "__main__":
    main()
