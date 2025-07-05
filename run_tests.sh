#!/bin/bash
# Check if Gradle wrapper exists, if not make it executable
if [ ! -x ./gradlew ]; then
    chmod +x ./gradlew
fi

# Run tests with Gradle
./gradlew test