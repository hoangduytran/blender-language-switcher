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

### Installing from source

If you've changed the source, rebuild the zip with the included script. It
needs Python 3.8 or newer and writes `dist/switch_language-<version>.zip`,
taking the version from `blender_manifest.toml`:

```sh
python3 mk_install_zip.py                        # auto-detect Blender, else plain zip
python3 mk_install_zip.py --blender /path/to/blender
python3 mk_install_zip.py --no-blender           # plain zip, no Blender needed
```

When the script can find Blender 4.2+, it builds and validates the package with
`blender --command extension build`. It looks in `--blender`, the `BLENDER`
environment variable, `blender` on `PATH`, and on macOS
`/Applications/Blender*.app`. If Blender isn't found, it writes the same zip
layout using Python alone. Then install the new zip as described above.

When you release a new version, bump `version` in `blender_manifest.toml` first
so the zip gets a new file name.

## Usage

1. Look at the right-hand end of the top bar, just before the **Scene** selector.
2. Pick a language from the dropdown.
3. Tick the checkbox to switch the UI to that language.
4. Untick it to go back to English.

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
