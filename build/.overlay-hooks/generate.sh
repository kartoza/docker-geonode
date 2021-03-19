#!/usr/bin/env bash
# input are given via stdin : <&0
# treat it as a file
# example:
# cat <&0

# In put is a json array like this:
#[
#  {
#    'template': <template-name>
#    'output': <destination-output-name>
#  }
#]

cat <&0