#!/bin/sh -e

# This script should be run from the root

final="static/mojang/library-patches.json"
lwjgl3="patches/generated/linux-lwjgl3.json"
static="patches/generated/static.json"
matches="patches/generated/matches.json"

tmp=$(mktemp)
jq -s 'add' "$matches" "$static" "$lwjgl3" > "$tmp"
mv "$tmp" "$final"