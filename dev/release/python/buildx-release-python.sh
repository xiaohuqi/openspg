docker buildx build -f Dockerfile --platform linux/arm64/v8,linux/amd64 --push \
  -t openspg/openspg-python:0.0.2-beta1 \
  -t openspg/openspg-python:latest \
  .
