#!/bin/bash
# Login-node wait helper (grep/squeue/sleep only): wait up to $1 seconds until every job id in $2 (comma list) has left
# the queue, or, with $3 = a file and $4 = an extended regex, until that file holds a line matching it. Prints the queue
# state at the end.
#   bash wait_for.sh 540 40431706,40431707
#   bash wait_for.sh 540 40431706 ~/logs/carmcv9i_40431706_0.out 'CV_DONE|RUN_FAILED'
T=${1:-540}; J=${2:-}; F=${3:-}; P=${4:-}
end=$(( $(date +%s) + T ))
while [ "$(date +%s)" -lt "$end" ]; do
  if [ -n "$F" ]; then
    grep -qE "$P" "$F" 2>/dev/null && break
  elif [ -n "$J" ]; then
    squeue -h -j "$J" 2>/dev/null | grep -q . || break
  fi
  sleep 30
done
date
[ -n "$J" ] && squeue -j "$J" -o "%.16i %.12j %.8T %.10M %.20R" 2>/dev/null
exit 0
