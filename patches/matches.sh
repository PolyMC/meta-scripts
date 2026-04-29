#!/bin/sh -e

# Generate matches for ARM platforms.

# shellcheck disable=SC1091
. ./common.sh

range="3.3.1-3.4.1"
versions="3.3.1 3.3.2 3.3.3 3.3.6 3.4.1"
platforms="windows-arm64 osx-arm64"

match_block() {
	platform="$1"
	comment="Add $platform support for LWJGL $range"

	shift
	match_arr=$(match_natives "$platform" "$@")
	overrides=$(override allow "$platform")

	jq -rn --arg comment "$comment" --argjson match "$match_arr" --argjson rules "$overrides" \
	'{_comment: $comment, match: $match, override: {rules: $rules}}'
}

# TODO(crueter): Move linux-arm64 stuff to a single block?
for platform in $platforms; do
	# shellcheck disable=SC2086
	match_block "$platform" $versions
done | jq -s '.' > generated/matches.json