#!/bin/bash

STAGE=$1
COMPONENT=$2

[ $# -eq 0 ] && {
    echo "Usage: $0 stage [component]"
    echo "  stage       - Deployment stage: development | production"
    echo "  component   - Optional: frontend-only | backend-only"
    exit 1
}

# Frontend
if [ "$COMPONENT" != 'frontend-only' ]; then
    echo
    echo "Building and packaging the backend . . ."
    echo "Using AWS CLI profile: $AWS_PROFILE"
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
    vue-cli-service build --mode "$STAGE"
    cd - || exit 1
fi

exit 0
