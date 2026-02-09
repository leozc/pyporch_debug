#!/usr/bin/env bash

set -euo pipefail

if ! command -v jq >/dev/null; then
    echo >&2 "You must have \`jq\` installed to run this script."
    exit 1
fi

grep -v -E "^//" 3rdparty/python/split.lock | jq '
    .locked_resolves[] | {
        marker: .marker,
        locked_requirements: [
            .locked_requirements[] | .project_name + "==" + .version
        ]
    }
'
