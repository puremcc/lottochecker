#!/bin/bash

COMPONENT=$2

[ $# -eq 0 ] && {
    echo "Usage: $0 stage [component]"
    echo "  component   - Optional: frontend-only | backend-only"
    exit 1
}

# Frontend
if [ "$COMPONENT" != 'frontend-only' ]; then
    echo
    echo "Building and packaging the backend . . ."
    if [ -v AWS_PROFILE ]; then echo "Using AWS CLI profile: $AWS_PROFILE"; fi
    cd backend || exit 1
    sam build
    sam package --s3-bucket "$SAM_BUCKET_NAME"
    cd - || exit 1
fi

# Backend
if [ "$COMPONENT" != 'backend-only' ]; then
    echo
    echo "Building the frontend . . ."
    cd frontend || exit 1
    npx vue-cli-service build
    cd - || exit 1
fi

exit 0
