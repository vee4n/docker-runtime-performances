#!/bin/bash
# scripts/measure-startup.sh
IMAGE=$1
TRIALS=30
OUTPUT="data/raw/startup-time.csv"

echo "image,trial,startup_time_ms" >> $OUTPUT

for i in $(seq 1 $TRIALS); do
  START=$(date +%s%3N)

  CONTAINER_ID=$(docker run -d -p 3000:3000 $IMAGE)

  # Poll until healthy
  until curl -sf http://localhost:3000/health > /dev/null; do
    sleep 0.1
  done

  END=$(date +%s%3N)
  DURATION=$((END - START))

  echo "$IMAGE,$i,$DURATION" >> $OUTPUT
  echo "Trial $i: ${DURATION}ms"

  # Cleanup
  docker stop $CONTAINER_ID
  docker rm $CONTAINER_ID
  sleep 5
done
