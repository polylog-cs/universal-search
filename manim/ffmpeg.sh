#!/bin/bash

fn="${@:$#}"
set -- "${@:1:$(($# - 1))}"
exec ffmpeg "$@" -crf 10 "$fn"
