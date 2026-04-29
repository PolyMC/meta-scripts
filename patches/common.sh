#!/bin/sh -e

# Mojang's servers do *not* provide Linux/ARM64 natives for LWJGL.
# So we have to add overrides that additionally download LWJGL's native libraries
# From their servers.

# check if version $1 is $2 or higher
version_gte() {
	v1=$1
	v2=$2

	# check each of the three fields
	[ "$v1" = "$(printf '%s\n%s' "$v1" "$v2" | sort -t. -k1,1n -k2,2n -k3,3n | tail -n 1)" ]
}

libs() {
	platform="$1"
	version="$2"

	_match="lwjgl-glfw lwjgl-jemalloc lwjgl-openal lwjgl-opengl lwjgl-stb lwjgl-tinyfd lwjgl"

	# freetype
	if version_gte "$version" "3.3.2"; then
		_match="lwjgl-freetype $_match"
	fi

	# vk
	if version_gte "$version" "3.4.1"; then
		_match="$_match lwjgl-shaderc lwjgl-spvc lwjgl-vma"

		if [ "$platform" = "macos-arm64" ]; then
			_match="$_match lwjgl-vulkan"
		fi
	fi

	echo "$_match"
}

# get the natives match array for this version/platform
# mainly used for arm stuff
match_natives() {
	platform="$1"
	# annoying
	if [ "$platform" = osx-arm64 ]; then platform=macos-arm64; fi
	shift

	for version in "$@"; do
		for lib in $(libs "$platform" "$version"); do
			echo "org.lwjgl:$lib-natives-$platform:$version"
		done
	done | jq -Rn '[inputs]'
}

# get the standard match array for this version
# mainly used for arm stuff
match() {
	for version in "$@"; do
		for lib in $(libs "$platform" "$version"); do
			echo "org.lwjgl:$lib:$version"
		done
	done | jq -Rn '[inputs]'
}

# override-rules allow/disallow platforms
override() {
	action="$1"
	shift 1
	for platform in "$@"; do
		jq -n --arg platform "$platform" --arg action "$action" '{action: $action, os: {name: $platform}}'
	done | jq -s '.'
}

# An artifact. duh
# Needs sha1sum, size, url
artifact() {
	url="$1"

	tmp=$(mktemp)
	curl -sL "$url" -o "$tmp" --fail
	sha1=$(sha1sum "$tmp" | awk '{print $1}')
	size=$(stat -c %s "$tmp")

	jq -n --arg url "$url" --arg sha1 "$sha1" --arg size "$size" \
		'{sha1: $sha1, size: ($size | tonumber), url: $url}'
}
