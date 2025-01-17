#!/usr/bin/env python
#
# Rebuild script for ligaturized fonts.
# Uses ligaturize.py to do the heavy lifting; this file basically just contains
# the mapping from input font paths to output fonts.

#### User configurable settings ####

# For the prefixed_fonts below, what word do we stick in front of the font name?
LIGATURIZED_FONT_NAME_PREFIX = "Liga"

# Should we copy some individual punctuations characters like &, ~, and <>,
# as well as ligatures? The full list is in ligatures.py.
COPY_CHARACTER_GLYPHS = False

# If copying individual characters, how different in width (relative to the font
# we're ligaturizing) should they be before we attempt to width-correct them?
# The default (0.1) means to width-correct if they're +/- 10%. Values >1.0
# effectively disable this feature.
SCALE_CHARACTER_GLYPHS_THRESHOLD = 0.1

#### Fonts that should be prefixed with "Liga" when ligaturized. ####
# Don't put fonts licensed under UFL here, and don't put fonts licensed under
# SIL OFL here either unless they haven't specified a Reserved Font Name.

prefixed_fonts = [
  # Apache 2.0 license

  # MIT license

  # SIL OFL with no Reserved Font Name
  'fonts/fira-italic/distr/otf/*.otf',
]

#### Fonts that need to be renamed. ####
# These are fonts that either have name collisions with the prefixed_fonts
# above, or are released under licenses that permit modification only if we
# change the name of the modified fonts.

renamed_fonts = {
  'fonts/hack/*.ttf': 'Liga Hack',
  # This doesn't have a reserved name, but if we don't rename it it'll collide
  # with its sibling Fantasque Sans Mono Normal, listed above.
  'fonts/FantasqueSansMono-NoLoopK/*.otf': 'Liga Fantasque Sans Mono NoLoopK',

  # SIL OFL with reserved name
  'fonts/plex/IBM-Plex-Mono/fonts/complete/ttf/*.ttf': 'LigaPlex Mono',
  'fonts/SourceCodeVariable*': 'LigaSrc Variable',

  # UFL
}

#### Fonts we can't ligaturize. ####
# Fonts that we can't ligaturize because their licences do not permit derivative
# works of any kind.
# Individual users may still be able to make ligaturized versions for personal
# use, but we can't check them into the repo or include them in releases.

# prefixed_fonts += [
#   'CamingoCode*',
#   'SFMono*',
# ]

#### No user serviceable parts below this line. ####

import sys
from glob import glob
from ligaturize import ligaturize_font

for pattern in prefixed_fonts:
  files = glob(pattern)
  if not files:
    print("Error: pattern '%s' didn't match any files." % pattern)
    sys.exit(1)
  for input_file in files:
    ligaturize_font(
      input_file, ligature_font_file=None, output_dir='fonts/output/',
      prefix=LIGATURIZED_FONT_NAME_PREFIX, output_name=None,
      copy_character_glyphs=COPY_CHARACTER_GLYPHS,
      scale_character_glyphs_threshold=SCALE_CHARACTER_GLYPHS_THRESHOLD)

for pattern,name in renamed_fonts.items():
  files = glob(pattern)
  if not files:
    print("Error: pattern '%s' didn't match any files." % pattern)
    sys.exit(1)
  for input_file in files:
    ligaturize_font(
      input_file, ligature_font_file=None, output_dir='fonts/output/',
      prefix=None, output_name=name,
      copy_character_glyphs=COPY_CHARACTER_GLYPHS,
      scale_character_glyphs_threshold=SCALE_CHARACTER_GLYPHS_THRESHOLD)
