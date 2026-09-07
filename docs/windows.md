# Running This Repo On Windows

Every command in this repo's docs is written as `python3`, which is correct on
macOS and Linux and **does not exist on Windows**. This page is the translation
layer. Nothing in the course code is POSIX-specific; the only differences are
how you name the interpreter, how you activate the virtual environment, and one
line-ending setting that is already handled for you.

Read the three-command version, then come back for the rest only if something
misbehaves.

## The short version

```powershell
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r examples\strongbench-expense-agent\requirements.txt
```

After that, **every `python3` in the README and in the level docs becomes
`python`.** That is the whole translation.

## Why `python3` fails here

The python.org Windows installer creates `python.exe` and the `py` launcher. It
does not create `python3.exe`. So `python3 -m evals.runner` fails on a normal
Windows install, even though the same command is correct on macOS.

Two consequences worth knowing:

- **Use `py -3` before the virtual environment exists.** The `py` launcher is
  the one interpreter name Windows guarantees, and it picks the right version
  when several are installed.
- **Use `python` once the virtual environment is active.** `.venv\Scripts\`
  contains `python.exe` but no `python3.exe`, so `python3` fails *even inside an
  activated venv*. This surprises people who expect activation to fix it.

### If typing `python` opens the Microsoft Store

Windows ships stub aliases for `python.exe` and `python3.exe` that open the
Store when no Python is installed. If you hit that, either install Python from
python.org, or turn the stubs off:

> Settings → Apps → Advanced app settings → App execution aliases → switch off
> **python.exe** and **python3.exe**

Installing Python *from* the Microsoft Store does create a real `python3.exe`,
which is why `python3` works on some Windows machines and not others. Do not
rely on it; the repo's docs assume you followed the short version above.

## Activating the virtual environment

Pick the row for the shell you actually use.

| Shell | Command |
| --- | --- |
| PowerShell | `.venv\Scripts\Activate.ps1` |
| Command Prompt (cmd.exe) | `.venv\Scripts\activate.bat` |
| Git Bash / WSL | `source .venv/bin/activate` (WSL) or `source .venv/Scripts/activate` (Git Bash) |

**If PowerShell refuses to run the activation script**, it is the execution
policy, not a problem with this repo. Either allow signed local scripts for your
own account:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

…or skip the policy change entirely and use Command Prompt instead. Both work.

## Translating the course commands

| The docs say | On Windows, run |
| --- | --- |
| `python3 run_agent.py --all --quiet` | `python run_agent.py --all --quiet` |
| `python3 -m strongbench_agent.check_traces traces/level-1.jsonl` | `python -m strongbench_agent.check_traces traces/level-1.jsonl` |
| `python3 -m evals.runner --model scripted` | `python -m evals.runner --model scripted` |
| `python3 -m evals.operations` | `python -m evals.operations` |
| `python3 -m datasets.strongbench` | `python -m datasets.strongbench` |
| `python3 -m model_improvement.strongbench` | `python -m model_improvement.strongbench` |
| `python3 -m model_improvement.strongbench.train_lora --dry-run` | `python -m model_improvement.strongbench.train_lora --dry-run` |
| `python3 -m environments.strongbench_finance` | `python -m environments.strongbench_finance` |
| `python3 -m rl_reliability.strongbench` | `python -m rl_reliability.strongbench` |
| `python3 integrations/prime-intellect/.../strongbench_finance_reliability.py` | `python integrations\prime-intellect\environments\strongbench_finance_reliability\strongbench_finance_reliability.py` |

Forward slashes in that last path work fine too — Python accepts them on
Windows. Use whichever you find readable.

## Line endings

This is the one Windows issue that could actually corrupt shared work, and
[`.gitattributes`](../.gitattributes) already handles it. Here is what it is
protecting you from, so you recognise it if it ever surfaces.

Every builder in this repo writes artifacts through Python's text mode, which
turns `\n` into `\r\n` on Windows. Meanwhile the repo requires generated bundles
to be byte-reproducible — Level 6 and Level 7 CI both run
`git diff --exit-code` after rebuilding, and fail the build if a single byte
moved. Without a line-ending policy, a Windows contributor rebuilding a bundle
could produce a whole-file diff containing no real change, or commit CRLF
artifacts that then fail CI on Linux.

`.gitattributes` pins `eol=lf` for every text file, so this is settled
regardless of your `core.autocrlf` setting.

**If you ever see a diff where every line changed but nothing looks different**,
that is a line-ending problem. Fix it with:

```powershell
git add --renormalize .
```

## Things that are *not* a Windows problem here

Listed so you do not go hunting for them:

- **Encodings.** Every `open()` in the course code pins `encoding="utf-8"`
  explicitly, so the old Windows cp1252 decode failure cannot happen.
- **Path handling.** The code uses `pathlib`, never hardcoded `/` separators.
- **Shell-outs.** There are none. No builder invokes a shell, `curl`, or a
  POSIX-only tool.
- **The offline model adapter.** No API key, no network, no platform-specific
  dependency. It behaves identically on Windows.

## Known rough edges

- **Compiled bytecode is currently tracked in git.** 27 `.pyc` files built by
  CPython 3.14 are committed. On another Python version you will generate
  differently-named `.pyc` files that show up as untracked. Harmless, but noisy.
  They should be removed from the index and ignored.
- **Long paths.** The deepest file here is about 95 characters, so you are well
  inside the 260-character limit unless you clone into an already-deep folder.
  If you hit a "filename too long" error, run
  `git config --global core.longpaths true`.

## Check your setup

Run this from the repository root with the virtual environment active. All of it
should pass, and the last command should print nothing.

```powershell
python -m pytest evals\tests datasets\tests model_improvement\tests environments\tests rl_reliability\tests
python -m environments.strongbench_finance
python -m rl_reliability.strongbench
python integrations\prime-intellect\environments\strongbench_finance_reliability\strongbench_finance_reliability.py
git diff --exit-code -- environments rl_reliability integrations
```

Expected: 38 tests pass, the two builders print their reports, the adapter
prints `OK: adapter loaded...`, and the `git diff` is silent. That last command
is scoped to the generated bundles — the same scope the Level 6 and Level 7 CI
workflows gate — so your own edits elsewhere will not trip it.

That last silence is the real test. It means your rebuild produced artifacts
byte-identical to the ones committed from macOS and Linux, which is exactly what
the course's reproducibility bar requires. If it prints a wall of changes,
re-read the line-endings section above.
