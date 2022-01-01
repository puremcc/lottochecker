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
    echo "Deploying the backend . . ."
    cd backend || exit 1
    sam deploy --config-env "$STAGE" \
        --parameter-overrides "AppHostUrl=$APP_HOST_URL"
    cd - || exit 1
fi

# Backend
if [ "$COMPONENT" != 'backend-only' ]; then
    echo
    echo "Deploying the frontend . . ."
    cd frontend || exit 1
    echo "Using AWS CLI credentials profile: $AWS_PROFILE"
    aws s3 sync \
        --delete dist/ "s3://$BUCKET_NAME" \
        --profile "$AWS_PROFILE"
    aws cloudfront create-invalidation \
        --distribution-id "$DISTRIBUTION_ID" \
        --paths "/*" \
        --profile "$AWS_PROFILE"
    cd - || exit 1
fi

exit 0
