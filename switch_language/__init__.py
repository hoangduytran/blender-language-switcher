# SPDX-FileCopyrightText: 2026 Blender Foundation
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Quick translation language switcher for the top bar."""

from __future__ import annotations

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
    "author": "Blender Translation Local Test",
    "version": (1, 0, 1),
    "blender": (4, 2, 0),
    "location": "Top Bar (next to Scene selector)",
    "description": "Quickly toggle Blender UI translation language from the top bar",
    "category": "Interface",
}


ADDON_ID = __package__ or __name__
_LANGUAGE_ITEMS_CACHE = []


def _rna_language_items(context):
    # Build the list from `bpy.app.translations.locales` rather than the static
    # `enum_items` of the `language` property: in Blender 4.5 the latter only
    # contains "DEFAULT", as the real items come from a dynamic callback.
    view = context.preferences.view
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
        context.preferences.view,
        addon_preferences.enabled,
        addon_preferences.language,
        _available_language_identifiers(context),
    )


def _preferences_update(self, context):
    _apply_addon_preferences(self, context)


class SWITCH_LANGUAGE_AddonPreferences(AddonPreferences):
    bl_idname = ADDON_ID

    language: EnumProperty(
        name="Language",
        description="Language to use while the quick switch is enabled",
        items=_language_enum_items,
        update=_preferences_update,
    )

    enabled: BoolProperty(
        name="Enable",
        description="Use the selected language and enable all translation options",
        default=False,
        update=_preferences_update,
    )


def draw_topbar_switch_language(self, context):
    # The top bar header draws twice: once for the left region (menus, workspaces)
    # and once for the right region (Scene, View Layer). Only draw on the right,
    # so the switcher sits just before the Scene selector.
    if context.region.alignment != 'RIGHT':
        return
    if not bpy.app.build_options.international:
        return

    addon_preferences = context.preferences.addons[ADDON_ID].preferences

    row = self.layout.row(align=True)
    row.ui_units_x = 8
    split = row.split(factor=0.84, align=True)
    split.prop(addon_preferences, "language", text="")
    split.prop(addon_preferences, "enabled", text="")


classes = (
    SWITCH_LANGUAGE_AddonPreferences,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.TOPBAR_HT_upper_bar.prepend(draw_topbar_switch_language)


def unregister():
    bpy.types.TOPBAR_HT_upper_bar.remove(draw_topbar_switch_language)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
