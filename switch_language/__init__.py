# SPDX-FileCopyrightText: 2026 Blender Foundation
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Quick translation language switcher for the top bar."""

import bpy
from bpy.props import BoolProperty, EnumProperty
from bpy.types import AddonPreferences

from .language_state import (
    DEFAULT_LANGUAGE_IDENTIFIER,
    ENGLISH_LANGUAGE_IDENTIFIER,
    apply_language_state,
)


bl_info = {
    "name": "Switch Language",
    "author": "Hoang Duy Tran <hoangduytran1960@googlemail.com>",
    "version": (1, 0, 3),
    "blender": (2, 78, 0),
    "location": "Top Bar / Info header",
    "description": "Quickly toggle Blender UI translation language from the top bar",
    "category": "Interface",
}


# Blender 2.8x rejects add-ons declaring a pre-2.80 API, even when compatible.
if bpy.app.version >= (2, 80, 0):
    bl_info["blender"] = (2, 80, 0)


ADDON_ID = __package__ or __name__
_LANGUAGE_ITEMS_CACHE = []


def _blender_preferences(context):
    """Return preferences using the API exposed by the running Blender."""
    if bpy.app.version < (2, 80, 0):
        return context.user_preferences
    return context.preferences


def _translation_preferences(context):
    """Locate translation settings, moved from System to Interface in 2.80."""
    preferences = _blender_preferences(context)
    if bpy.app.version < (2, 80, 0):
        return preferences.system
    return preferences.view


def _header_type():
    """Choose the pre-2.80 Info header or the modern top bar."""
    if bpy.app.version < (2, 80, 0):
        return bpy.types.INFO_HT_header
    return bpy.types.TOPBAR_HT_upper_bar


def _rna_language_items(context):
    # Build the list from `bpy.app.translations.locales` rather than the static
    # `enum_items` of the `language` property: in Blender 4.5 the latter only
    # contains "DEFAULT", as the real items come from a dynamic callback.
    view = _translation_preferences(context)
    enum_item_name = bpy.types.UILayout.enum_item_name
    enum_item_description = bpy.types.UILayout.enum_item_description
    identifiers = (DEFAULT_LANGUAGE_IDENTIFIER, *bpy.app.translations.locales)
    return tuple(
        (
            identifier,
            enum_item_name(view, "language", identifier) or identifier,
            enum_item_description(view, "language", identifier) or "",
        )
        for identifier in identifiers
    )


def _available_language_identifiers(context):
    return tuple(identifier for identifier, _name, _description in _rna_language_items(context))


def _language_enum_items(_self, context):
    global _LANGUAGE_ITEMS_CACHE

    items = [
        item
        for item in _rna_language_items(context or bpy.context)
        if item[0] != DEFAULT_LANGUAGE_IDENTIFIER
    ]
    items = [
        item for item in items if item[0] == ENGLISH_LANGUAGE_IDENTIFIER
    ] + [
        item for item in items if item[0] != ENGLISH_LANGUAGE_IDENTIFIER
    ]
    if not items:
        items = [
            (
                ENGLISH_LANGUAGE_IDENTIFIER,
                "English (US)",
                "Locale code: en_US",
            ),
        ]

    _LANGUAGE_ITEMS_CACHE = items
    return _LANGUAGE_ITEMS_CACHE


def _apply_addon_preferences(addon_preferences, context):
    if not bpy.app.build_options.international:
        return

    apply_language_state(
        _translation_preferences(context),
        addon_preferences.enabled,
        addon_preferences.language,
        _available_language_identifiers(context),
    )


def _preferences_update(self, context):
    _apply_addon_preferences(self, context or bpy.context)


class SWITCH_LANGUAGE_AddonPreferences(AddonPreferences):
    bl_idname = ADDON_ID

    language = EnumProperty(
        name="Language",
        description="Language to use while the quick switch is enabled",
        items=_language_enum_items,
        update=_preferences_update,
    )

    enabled = BoolProperty(
        name="Enable",
        description="Use the selected language and enable all translation options",
        default=False,
        update=_preferences_update,
    )


# Python 3.5 cannot parse property annotations. Convert assignment-style
# definitions to Blender 2.80+'s annotation storage before registration.
if bpy.app.version >= (2, 80, 0):
    SWITCH_LANGUAGE_AddonPreferences.__annotations__ = {
        name: SWITCH_LANGUAGE_AddonPreferences.__dict__[name]
        for name in ("language", "enabled")
    }
    del SWITCH_LANGUAGE_AddonPreferences.language
    del SWITCH_LANGUAGE_AddonPreferences.enabled


def draw_topbar_switch_language(self, context):
    # The top bar header draws twice: once for the left region (menus, workspaces)
    # and once for the right region (Scene, View Layer). Only draw on the right,
    # so the switcher sits just before the Scene selector.
    if bpy.app.version >= (2, 80, 0) and context.region.alignment != 'RIGHT':
        return
    if not bpy.app.build_options.international:
        return

    addon_preferences = _blender_preferences(context).addons[ADDON_ID].preferences

    row = self.layout.row(align=True)
    row.ui_units_x = 8
    if bpy.app.version < (2, 80, 0):
        split = row.split(percentage=0.84, align=True)
    else:
        split = row.split(factor=0.84, align=True)
    split.prop(addon_preferences, "language", text="")
    split.prop(addon_preferences, "enabled", text="")


classes = (
    SWITCH_LANGUAGE_AddonPreferences,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    _header_type().prepend(draw_topbar_switch_language)


def unregister():
    _header_type().remove(draw_topbar_switch_language)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
