# SPDX-FileCopyrightText: 2026 Blender Foundation
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""State helpers for the Switch Language add-on."""

from __future__ import annotations


DEFAULT_LANGUAGE_IDENTIFIER = "DEFAULT"
ENGLISH_LANGUAGE_IDENTIFIER = "en_US"
TRANSLATION_OPTION_NAMES = (
    "use_translate_tooltips",
    "use_translate_interface",
    "use_translate_reports",
    "use_translate_new_dataname",
)


def choose_off_language(available_languages):
    """Return the language Blender should use when quick switching is disabled."""
    available_languages = tuple(available_languages)
    if DEFAULT_LANGUAGE_IDENTIFIER in available_languages:
        return DEFAULT_LANGUAGE_IDENTIFIER
    if ENGLISH_LANGUAGE_IDENTIFIER in available_languages:
        return ENGLISH_LANGUAGE_IDENTIFIER
    if available_languages:
        return available_languages[0]
    return DEFAULT_LANGUAGE_IDENTIFIER


def choose_on_language(selected_language, available_languages):
    """Return a valid language for the enabled switch state."""
    available_languages = tuple(available_languages)
    if not available_languages or selected_language in available_languages:
        return selected_language
    if ENGLISH_LANGUAGE_IDENTIFIER in available_languages:
        return ENGLISH_LANGUAGE_IDENTIFIER
    for language in available_languages:
        if language != DEFAULT_LANGUAGE_IDENTIFIER:
            return language
    return choose_off_language(available_languages)


def resolve_target_language(enabled, selected_language, available_languages):
    """Choose the language identifier for the requested switch state."""
    if enabled:
        return choose_on_language(selected_language, available_languages)
    return choose_off_language(available_languages)


def set_translation_options(view, enabled):
    """Set all translation usage flags on a Blender preferences view object."""
    for option_name in TRANSLATION_OPTION_NAMES:
        setattr(view, option_name, enabled)


def apply_language_state(view, enabled, selected_language, available_languages):
    """Apply the quick-switch language state to a Blender preferences view object."""
    target_language = resolve_target_language(enabled, selected_language, available_languages)

    if enabled:
        view.language = target_language
        set_translation_options(view, True)
    else:
        set_translation_options(view, False)
        view.language = target_language

    return target_language
