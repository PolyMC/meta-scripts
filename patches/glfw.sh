#!/bin/sh -e

# shellcheck disable=SC1091
. ./common.sh

platforms="generic linux macos macos-arm64 windows windows-x86 windows-arm64"

# Adds GLFW to LWJGL 3.4.1. Used by versions <26.3-snapshot-4
# Exotic Linux arches/FreeBSD are already covered elsewhere
glfw_allow() {
	platform="$1"
	version="3.4.1"
	lib="lwjgl-glfw"

	# used for rules matching
	case "$platform" in
		macos*) os=$(echo "$platform" | sed 's/macos/osx/') ;;
		windows-x86) os=windows ;;
		*) os="$platform" ;;
	esac

	# artifact naming
	case "$platform" in
		generic)
			artifact="$lib-$version"
			_name="$lib" ;;
		*)
			artifact="$lib-$version-natives-$platform"
			_name="$lib-natives-$platform" ;;
	esac

	# name used to match
	name="org.lwjgl:$_name:$version"

	# construct json
	url="https://libraries.minecraft.net/org/lwjgl/$lib/$version/$artifact.jar"

	artifact=$(artifact "$url")

	json=$(jq -n --argjson artifact "$artifact" --arg name "$name" \
		'{downloads: {artifact: $artifact}, name: $name}')

	# add whitelist for natives
	if [ "$platform" != "generic" ]; then
		rules=$(override allow "$os")
		json=$(printf '%s' "$json" | jq --argjson rules "$rules" '.rules = $rules')
	fi

	echo "$json"
}

# all platforms
glfw_libs() {
	for platform in $platforms; do
		glfw_allow "$platform"
	done | jq -s '.'
}

# lwjgl and unsafe
glfw_matches() {
	echo "org.lwjgl:lwjgl:3.4.1"
	echo "org.lwjgl:lwjgl:3.4.1:unsafe"
}

comment="Add glfw to LWJGL 3.4.1"
matches=$(glfw_matches | jq -Rn '[inputs]')
libs=$(glfw_libs)

jq -n --argjson libs "$libs" --argjson match "$matches" --arg comment "$comment" \
	'[{_comment: $comment, match: $match, additionalLibraries: $libs, patchAdditionalLibraries: true}]' \
	> generated/glfw.json
