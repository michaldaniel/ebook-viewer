#!/bin/sh
find . -name "*.py" | xargs pygettext3.4 -d po/messages
