#!/bin/sh -e

# Generate LWJGL3 linux ARM/RISCV overrides.

# shellcheck disable=SC1091
. ./common.sh

versions="3.3.1 3.3.2 3.3.3 3.3.6 3.4.1"
platforms="linux-arm64 linux-arm32 linux-riscv64 freebsd"

# TODO(crueter): See if these need to be made separate.
libraries() {
	platform="$1"
	version="$2"

	for lib in $(libs "$platform" "$version"); do
		# TODO(crueter): make into common funcs?
		# lwjgl jemalloc for 3.3.1 needs to be patched for 16kb page size (asahi)
		# only affects linux-arm64
		if [ "$lib" = "lwjgl-jemalloc" ] && [ "$version" = "3.3.1" ] && [ "$platform" = "linux-arm64" ]; then
			name="org.lwjgl:$lib-natives-$platform:$version-gman64.3"
			url="https://github.com/theofficialgman/lwjgl3-binaries-arm64/raw/lwjgl-$version/lwjgl-jemalloc-patched-natives-$platform.jar"
		else
			name="org.lwjgl:$lib-natives-$platform:$version-lwjgl.1"
			url="https://build.lwjgl.org/release/$version/bin/$lib/$lib-natives-$platform.jar"
		fi
		rules=$(override allow "$platform")

		artifact=$(artifact "$url")

		jq -n --argjson artifact "$artifact" --argjson rules "$rules" --arg name "$name" \
			'{downloads: {artifact: $artifact}, name: $name, rules: $rules}'
	done | jq -s '.'
}

matches() {
	platform="$1"
	version="$2"

	comment="Add $platform support for LWJGL $version"
	matches=$(match "$version")
	libs=$(libraries "$platform" "$version")

	jq -n --argjson libs "$libs" --argjson match "$matches" --arg comment "$comment" \
		'{_comment: $comment, match: $match, additionalLibraries: $libs}'
}

for platform in $platforms; do
	for version in $versions; do
		# linux-riscv64 and freebsd only have builds available on 3.3.6+
		# Maybe someone wants to provide their own? :)
		echo "$platform: $version" >&2
		if { [ "$platform" = "linux-riscv64" ] || [ "$platform" = "freebsd" ]; } && ! version_gte "$version" "3.3.6"; then
			continue
		fi
		matches "$platform" "$version"
	done
done | jq -s '.' > generated/linux-lwjgl3.json