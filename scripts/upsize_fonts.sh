#!/usr/bin/env bash
# Usage: bash upsize_fonts.sh input.dot > output.dot
#
# Increases all font sizes and adjusts spacing/node sizes for
# better readability in EPS output.
#
# Font size mappings:
#   9  -> 13  (edge xlabels)
#   10 -> 14  (legend table)
#   11 -> 15  (most node labels)
#   12 -> 16  (diamond/octagon nodes, legend cluster)
#   13 -> 17  (gold star node)
#   16 -> 20  (cluster/subgraph titles)
#
# NOTE: substitutions are ordered largest-first to prevent
# a newly written value from being matched by a later rule
# (e.g. 12->16 must not then be caught by 16->20).

sed \
  -e 's/fontsize=20/fontsize=40/g' \
  -e 's/fontsize=18/fontsize=36/g' \
  -e 's/fontsize=17/fontsize=34/g' \
  -e 's/fontsize=16/fontsize=32/g' \
  -e 's/fontsize=15/fontsize=30/g' \
  -e 's/fontsize=14/fontsize=28/g' \
  -e 's/fontsize=13/fontsize=26/g' \
  -e 's/fontsize=12/fontsize=24/g' \
  -e 's/fontsize=11/fontsize=15/g' \
  -e 's/fontsize=10/fontsize=14/g' \
  -e 's/fontsize=9\b/fontsize=13/g' \
  -e 's/fontname="Helvetica";/fontname="Helvetica";\n    fontsize=18;/' \
  -e 's/nodesep=0\.7/nodesep=1.0/' \
  -e 's/ranksep=1\.2/ranksep=1.6/' \
  -e 's/arrowsize=0\.8/arrowsize=1.0/' \
  -e 's/width=2\.5/width=3.0/g' \
  -e 's/height=2\.5/height=3.0/g' \
  -e 's/width=2\.2/width=2.6/' \
  -e 's/height=1\.2/height=1.5/' \
  -e 's/width=2,/width=2.4,/' \
  "$@"
