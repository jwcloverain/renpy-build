#!/bin/bash

update () {
    remote="$1"
    dir="${2:-.}"
    branch="${3:-$BRANCH}"
    path="$BASE/$dir"

    if [ -d "$path/.git" ]; then
        pushd "$path"
        git remote set-url origin "$remote"
        git fetch origin "$branch:refs/remotes/origin/$branch"
        git checkout -B "$branch" "origin/$branch"
        popd
    else
        git clone --branch "$branch" "$remote" "$path"
    fi
}

BRANCH="${BRANCH:-$(git branch --show-current)}"
if [ -z "$BRANCH" ]; then
    echo "BRANCH must be set when HEAD is detached." >&2
    exit 1
fi

# The build repository follows BRANCH; each dependency can use its own branch.
update "$(git remote get-url origin)" . "$BRANCH"
update https://github.com/jwcloverain/renpy renpy "${RENPY_BRANCH:-$BRANCH}"
update https://github.com/jwcloverain/pygame_sdl2 pygame_sdl2 "${PYGAME_SDL2_BRANCH:-$BRANCH}"
update https://github.com/jwcloverain/renpyweb renpyweb "${RENPYWEB_BRANCH:-$BRANCH}"

rm -Rf "$BASE/renpy/module/gen"
rm -Rf "$BASE/renpy/module/gen3"
rm -Rf "$BASE/renpy/module/gen-static"
rm -Rf "$BASE/renpy/module/gen30-static"

rm -Rf "$BASE/pygame_sdl2/gen"
rm -Rf "$BASE/pygame_sdl2/gen3"
rm -Rf "$BASE/pygame_sdl2/gen-static"
rm -Rf "$BASE/pygame_sdl2/gen3-static"
