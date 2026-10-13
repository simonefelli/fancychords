#!/bin/bash
#
# Copyright (C) 2026 Simone Felli
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.

# Make the release archive of one platform: the executables plus everything
# a user needs to start (font, examples, licence, README.txt).
#
# usage: packaging/make_release_archive.sh BIN_DIR PLATFORM VERSION OUT_DIR
#   BIN_DIR   folder with the executables (fancychords, fancyscales or .exe)
#   PLATFORM  linux-amd64 or windows-amd64
#   VERSION   ie v0.8 (the git tag)
#   OUT_DIR   where the archive is written
# result: OUT_DIR/fancychords-PLATFORM-VERSION.tar.xz (Linux) or .zip (Windows),
# with everything inside a fancychords-PLATFORM-VERSION folder:
#   fancychords, fancyscales   the executables
#   font/                      the FChords font and its licence files
#   examples/                  d_form.txt and config_scales.json
#   LICENSE                    GPL version 3
#   README.txt                 install and quick start (packaging/release_readme.txt)
#
# Run from anywhere: paths are taken from the repository of this script.

set -euo pipefail

if [ $# -ne 4 ]; then
    echo "usage: $0 BIN_DIR PLATFORM VERSION OUT_DIR" >&2
    exit 1
fi
bin_dir=$1
platform=$2
version=$3
out_dir=$4

repo="$(cd "$(dirname "$0")/.." && pwd)"
name="fancychords-$platform-$version"
case "$platform" in
    windows-*) exe='.exe' ;;
    *)         exe='' ;;
esac

# stage everything in a fresh temporary folder
stage="$(mktemp -d)"
trap 'rm -r "$stage"' EXIT
dst="$stage/$name"
mkdir -p "$dst/font" "$dst/examples"

for prog in fancychords fancyscales; do
    cp "$bin_dir/$prog$exe" "$dst/"
    chmod +x "$dst/$prog$exe"
done
cp "$repo"/fonts/ubuntu-mono-derivative-fchords/* "$dst/font/"
cp "$repo/assets/d_form.txt" "$repo/assets/config_scales.json" "$dst/examples/"
cp "$repo/LICENSE" "$dst/"
sed -e "s/@VERSION@/$version/g" \
    -e "s/@PLATFORM@/$platform/g" \
    -e "s/@FANCYCHORDS@/$(printf '%-16s' "fancychords$exe")/" \
    -e "s/@FANCYSCALES@/$(printf '%-16s' "fancyscales$exe")/" \
    "$repo/packaging/release_readme.txt" > "$dst/README.txt"

mkdir -p "$out_dir"
out_dir="$(cd "$out_dir" && pwd)"
if [ -n "$exe" ]; then
    # Windows: zip, text files with Windows line endings
    for f in README.txt LICENSE; do
        sed -i 's/\r*$/\r/' "$dst/$f"
    done
    rm -f "$out_dir/$name.zip"
    (cd "$stage" && zip -q -9 -r "$out_dir/$name.zip" "$name")
    echo "$out_dir/$name.zip"
else
    tar -C "$stage" -cJf "$out_dir/$name.tar.xz" "$name"
    echo "$out_dir/$name.tar.xz"
fi
