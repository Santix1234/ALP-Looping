#!/bin/bash
# Android/Kotlin Project Test Runner

# Check for Kotlin and Android test files
KOTLIN_TEST_FILES=$(find . -name "*Test.kt")
JAVA_TEST_FILES=$(find . -name "*Test.java")

if [ -n "$KOTLIN_TEST_FILES" ] || [ -n "$JAVA_TEST_FILES" ]; then
    echo "Kotlin/Android test files found. Running tests..."
    
    # Try multiple test runners
    if command -v ./gradlew &> /dev/null; then
        echo "Using Gradle wrapper"
        ./gradlew test
    elif command -v gradle &> /dev/null; then
        echo "Using system Gradle"
        gradle test
    elif command -v mvn &> /dev/null; then
        echo "Using Maven"
        mvn test
    else
        echo "No suitable test runner found"
        exit 1
    fi
else
    echo "No Kotlin/Java test files found"
    exit 1
fi