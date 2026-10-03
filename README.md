# Blender Language Switcher

**English** | [Tiếng Việt](README_VI.md)

A small Blender add-on that puts a **language switcher in the top bar**, so you can
flip the whole UI between English and another language with one click, without
digging through *Preferences → Interface → Translation*.

It is handy for translators checking their work, for people learning Blender in
their own language who need to match English tutorials, and for anyone who
wants to look up the original English name of a menu item or tool.

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ File Edit Render Window Help │ Layout Modeling … │ [Français     ▾][✓] Scene │
└──────────────────────────────────────────────────────────────────────────────┘
                                                      └── the switcher ──┘
```

## Download version 1.0.3

| Blender version | Package |
|---|---|
| 2.78–4.1 | [switch_language-1.0.3-support_legacy.zip](https://github.com/hoangduytran/blender-language-switcher/releases/download/v1.0.3/switch_language-1.0.3-support_legacy.zip) |
| 4.2+ | [switch_language-1.0.3.zip](https://github.com/hoangduytran/blender-language-switcher/releases/download/v1.0.3/switch_language-1.0.3.zip) |

The legacy package also supports newer Blender versions through the add-on
installer. Both packages contain the same language-switching code. Install one.
Support starts at Blender 2.78; versions before 2.78 are not supported, and
future Blender releases may require updates.

Version 1.0.3 adds compatibility with Blender 2.78c and its Python 3.5 runtime,
while retaining the fixes for Blender 2.83 and newer versions.

## Features

- A language dropdown and an on/off checkbox in the top bar, just left of the
  **Scene** selector.
- **Checkbox on:** switches Blender to the chosen language and turns on every
  translation option available in that Blender (interface, tooltips, reports,
  new data names).
- **Checkbox off:** turns all translation options off and returns Blender to its
  default language, so the UI is in English again.
- The language list comes from the locales in your Blender build. English is
  listed first.
- Your chosen language is stored in the add-on preferences, so each time you
  switch back on you get the same language.

## Requirements

- Blender **2.78 or newer**. Use the legacy add-on ZIP for Blender 2.78–4.1,
  or the extension ZIP for Blender 4.2+. Tested with 2.78c, 2.83.9, 4.5.9, 5.2.0,
  and 5.3.0 Alpha. Translation options are detected from
  the running Blender version; older versions omit the reports option.
- A Blender build with international support. All official builds have it. If
  your build doesn't, the switcher stays hidden.

## Installation

### Blender 2.78–4.1 (including 2.83)

1. Download the legacy package from the table above or the [`dist/`](dist/) folder.
2. Open **Edit → Preferences → Add-ons → Install…** and select the ZIP.
3. Enable **Interface: Switch Language**.

For Blender 2.78–2.79, use **File → User Preferences → Add-ons → Install from
File…**. The switcher appears at the start of the Info header (the main menu
bar), rather than beside the Scene selector.

The legacy ZIP also works in newer Blender versions through **Add-ons → Install
from Disk…**. Install either the legacy add-on or the extension, not both.

### Blender 4.2+ (extension)

1. Download `switch_language-1.0.3.zip` from the [`dist/`](dist/) folder (click
   the file, then **Download raw file**). You can also get it from the
   [Releases](../../releases) page.
2. In Blender, open **Edit → Preferences → Get Extensions**.
3. Open the **⌄** menu in the top-right corner and choose **Install from Disk…**
4. Select the downloaded zip. The extension installs and enables itself.

You can also drag and drop the zip file onto the Blender window.

## Usage

1. Find the switcher just before the **Scene** selector in Blender 2.80+, or at
   the start of the main menu bar in Blender 2.78–2.79.
2. Pick a language from the dropdown.
3. Tick the checkbox to switch the UI to that language.
4. Untick it to go back to English.

## Changing the add-on and building your own zip

The `mk_install_zip.py` script turns the files in `switch_language/` into an
extension ZIP and a legacy add-on ZIP. Use it after you change the code, for example to fix a bug or
to change the default language, and want to install your own version.

You need **Python 3.8 or newer** and a copy of this repository.

### 1. Get the source

With Git:

```sh
git clone https://github.com/hoangduytran/blender-language-switcher.git
cd blender-language-switcher
```

Without Git, click **Code → Download ZIP** on the GitHub page, unzip it, and
open a terminal in the unzipped folder.

### 2. Make your changes

Edit the files in `switch_language/`:

- `__init__.py` draws the switcher in the top bar and stores its settings.
- `language_state.py` decides which language to use and turns the translation
  options on or off.
- `blender_manifest.toml` holds the name, version and minimum Blender version.

If you plan to share your build, increase `version` in `blender_manifest.toml`
(for example `1.0.1` → `1.0.3`). The zip is named after this version, and a
higher number lets Blender treat it as an update.

### 3. Build the zip

Run the script from the repository folder.

macOS / Linux:

```sh
python3 mk_install_zip.py
```

Windows (Command Prompt or PowerShell):

```bat
py mk_install_zip.py
```

The ZIPs are written to `dist/switch_language-<version>.zip` and
`dist/switch_language-<version>-support_legacy.zip`. The last line
of output shows its exact name:

```
Created dist/switch_language-1.0.3.zip (3 files: blender_manifest.toml, __init__.py, language_state.py)
```

By default the script looks for Blender. If it finds Blender 4.2 or newer, it
builds the extension with Blender's own builder and validates the package. It looks in these places, in order:

1. the `--blender` option,
2. the `BLENDER` environment variable,
3. `blender` on your `PATH`,
4. on macOS, `/Applications/Blender*.app`.

If Blender is older than 4.2 or isn't found, the extension ZIP is created with
Python alone. The script always creates a legacy ZIP with the `switch_language/`
folder at its root and no extension manifest. The extension keeps the 4.2 minimum
required by Blender's extension system; legacy metadata allows Blender 2.78+.

Options:

| Command | What it does |
|---------|--------------|
| `python3 mk_install_zip.py` | Uses Blender if it can find it, otherwise plain Python |
| `python3 mk_install_zip.py --blender PATH` | Uses the Blender at `PATH`, e.g. `"C:\Program Files\Blender Foundation\Blender 4.5\blender.exe"` or `/Applications/Blender.app/Contents/MacOS/Blender` |
| `python3 mk_install_zip.py --no-blender` | Never uses Blender; plain Python only |
| `python3 mk_install_zip.py --help` | Shows these options |

### 4. Install your zip

Install the new file from `dist/` as described in [Installation](#installation).
If an older version is already installed, Blender replaces it. Restart Blender
if the top bar doesn't update.

## How it works

The add-on registers a draw function on `TOPBAR_HT_upper_bar` using `prepend`.
Blender draws the top bar in two regions, left and right, and the function only
draws in the right-hand region (`context.region.alignment == 'RIGHT'`). In Blender 2.78–2.79 it uses `INFO_HT_header`, reads
`user_preferences.system`, and draws without the right-region filter. Because
it was prepended, the switcher appears just before the Scene / View Layer
selectors.

The dropdown and checkbox are properties of the add-on preferences. When either
one changes, `language_state.apply_language_state()` sets
`Preferences.view.language` and the `use_translate_*` options.

## Files

| Path | Purpose |
|------|---------|
| `switch_language/__init__.py` | Registration, preferences, top bar drawing |
| `switch_language/language_state.py` | Logic for choosing the language and applying the translation options |
| `switch_language/blender_manifest.toml` | Extension manifest |
| `dist/switch_language-1.0.3.zip` | Extension package for Blender 4.2+ |
| `dist/switch_language-1.0.3-support_legacy.zip` | Add-on package for Blender 2.78+ |
| `mk_install_zip.py` | Rebuilds the zip in `dist/` from the source |
| `README_VI.md` | This guide in Vietnamese |

## License

GPL-2.0-or-later. See [LICENSE](LICENSE).

## Compatibility checks

Run each installed Blender with factory settings, without saving preferences:

```sh
/Applications/Blender_283.app/Contents/MacOS/Blender --background --factory-startup --python-exit-code 1 --python tests/blender_smoke.py
```

This checks registered properties, language callbacks, supported translation
flags, header controls, disabling, and re-registration. Blender versions before
2.78 are outside the tested support range.
