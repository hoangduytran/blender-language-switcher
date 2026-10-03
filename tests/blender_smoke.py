"""Run with Blender --background --factory-startup --python this_file."""

import sys
from pathlib import Path
from types import SimpleNamespace

import addon_utils
import bpy


def main():
    """Verify registration, actual preference callbacks, and header drawing."""
    if '--' in sys.argv:
        archive_path = sys.argv[sys.argv.index('--') + 1]
        if bpy.app.version < (2, 80, 0):
            bpy.ops.wm.addon_install(filepath=archive_path)
        else:
            bpy.ops.preferences.addon_install(filepath=archive_path)
    else:
        sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    module = addon_utils.enable('switch_language', default_set=True)
    assert module is not None, 'Add-on enable failed'
    blender_preferences = module._blender_preferences(bpy.context)
    preferences = blender_preferences.addons['switch_language'].preferences
    view = module._translation_preferences(bpy.context)
    assert 'language' in preferences.bl_rna.properties
    assert 'enabled' in preferences.bl_rna.properties
    identifiers = module._available_language_identifiers(bpy.context)
    assert 'en_US' in identifiers
    language = 'vi_VN' if 'vi_VN' in identifiers else next(
        item for item in identifiers if item not in ('DEFAULT', 'en_US')
    )
    preferences.language = language
    preferences.enabled = True
    assert view.language == language, (view.language, language)
    flags = [name for name in (
        "use_translate_tooltips", "use_translate_interface",
        "use_translate_reports", "use_translate_new_dataname",
    )
             if name in view.bl_rna.properties]
    assert all(getattr(view, name) for name in flags)
    preferences.language = 'en_US'
    assert view.language == 'en_US'
    preferences.enabled = False
    assert view.language == 'DEFAULT'
    assert all(not getattr(view, name) for name in flags)
    items = module._language_enum_items(preferences, None)
    assert items[0][0] == 'en_US'
    assert len({item[0] for item in items}) == len(items)
    layout = RecordingLayout()
    context = SimpleNamespace(region=SimpleNamespace(alignment='RIGHT'),
                              preferences=blender_preferences, user_preferences=blender_preferences)
    module.draw_topbar_switch_language(SimpleNamespace(layout=layout), context)
    assert layout.properties == ['language', 'enabled']
    context.region.alignment = 'LEFT'
    module.draw_topbar_switch_language(SimpleNamespace(layout=layout), context)
    expected = ['language', 'enabled']
    if bpy.app.version < (2, 80, 0):
        expected *= 2
    assert layout.properties == expected
    addon_utils.disable('switch_language', default_set=True)
    assert 'switch_language' not in blender_preferences.addons
    module.register()
    module.unregister()
    sys.stdout.write('PASS Blender {}: callbacks, {} flags, header, re-registration\n'.format(
        bpy.app.version_string, len(flags)))
    sys.stdout.flush()


class RecordingLayout:
    """Record the header controls while checking their registered RNA names."""

    def __init__(self):
        self.properties = []

    def row(self, **kwargs):
        return self

    def split(self, **kwargs):
        return self

    def prop(self, preferences, name, **kwargs):
        assert name in preferences.bl_rna.properties
        self.properties.append(name)


if __name__ == '__main__':
    main()
