#!/bin/bash
# scripts/measure-pull.sh
IMAGE=$1
TRIALS=30
OUTPUT="data/raw/pull-time.csv"

echo "image,trial,pull_time_ms" >> $OUTPUT

for i in $(seq 1 $TRIALS); do
  # Remove image to force fresh pull
  docker rmi $IMAGE 2>/dev/null

  START=$(date +%s%3N)
  docker pull $IMAGE
  END=$(date +%s%3N)

  DURATION=$((END - START))
  echo "$IMAGE,$i,$DURATION" >> $OUTPUT
  echo "Trial $i: ${DURATION}ms"

  sleep 5  # cooldown between trials
done
