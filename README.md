# Blender Language Switcher

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

## Features

- A language dropdown and an on/off checkbox in the top bar, just left of the
  **Scene** selector.
- **Checkbox on:** switches Blender to the chosen language and turns on every
  translation option (interface, tooltips, reports, new data names).
- **Checkbox off:** turns all translation options off and returns Blender to its
  default language, so the UI is in English again.
- The language list comes from the locales in your Blender build. English is
  listed first.
- Your chosen language is stored in the add-on preferences, so each time you
  switch back on you get the same language.

## Requirements

- Blender **4.2 or newer**, since this is packaged as a Blender extension. It has
  been tested with Blender 4.5.
- A Blender build with international support. All official builds have it. If
  your build doesn't, the switcher stays hidden.

## Installation

1. Download `switch_language-1.0.1.zip` from the [`dist/`](dist/) folder (click
   the file, then **Download raw file**). You can also get it from the
   [Releases](../../releases) page.
2. In Blender, open **Edit → Preferences → Get Extensions**.
3. Open the **⌄** menu in the top-right corner and choose **Install from Disk…**
4. Select the downloaded zip. The extension installs and enables itself.

You can also drag and drop the zip file onto the Blender window.

## Usage

1. Look at the right-hand end of the top bar, just before the **Scene** selector.
2. Pick a language from the dropdown.
3. Tick the checkbox to switch the UI to that language.
4. Untick it to go back to English.

## Changing the add-on and building your own zip

The `mk_install_zip.py` script turns the files in `switch_language/` into an
installable zip. Use it after you change the code, for example to fix a bug or
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
(for example `1.0.1` → `1.0.2`). The zip is named after this version, and a
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

The zip is written to `dist/switch_language-<version>.zip`, and the last line
of output shows its exact name:

```
Created dist/switch_language-1.0.2.zip (3 files: blender_manifest.toml, __init__.py, language_state.py)
```

By default the script looks for Blender. If it finds one, it builds the
package with Blender's own extension builder and checks that the package is
valid. It looks in these places, in order:

1. the `--blender` option,
2. the `BLENDER` environment variable,
3. `blender` on your `PATH`,
4. on macOS, `/Applications/Blender*.app`.

If Blender isn't found, the script creates the zip with Python alone. That zip
has the same contents, but Blender hasn't checked it.

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
draws in the right-hand region (`context.region.alignment == 'RIGHT'`). Because
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
| `dist/switch_language-1.0.1.zip` | Ready-to-install extension package |
| `mk_install_zip.py` | Rebuilds the zip in `dist/` from the source |

## License

GPL-2.0-or-later. See [LICENSE](LICENSE).
