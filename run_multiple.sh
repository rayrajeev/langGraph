#!/bin/bash

# Multi-instance launcher for LangGraph Chat
echo "🚀 Starting multiple LangGraph chat instances..."

# Function to run chat instance
run_chat() {
    local instance_name=$1
    echo "Starting $instance_name..."
    osascript -e "tell application \"Terminal\" to do script \"cd $(pwd) && python src/agent/main.py\""
}

# Check if number of instances is provided
INSTANCES=${1:-2}

echo "Creating $INSTANCES chat instances..."

for i in $(seq 1 $INSTANCES); do
    run_chat "Chat Instance $i"
    sleep 1
done

echo "✅ All instances started!"
echo "Check your Terminal app for the chat windows."