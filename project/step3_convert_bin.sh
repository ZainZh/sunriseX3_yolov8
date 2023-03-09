#!/bin/bash

# check
hb_mapper checker \
  --model-type onnx \
  --model yolov8n.onnx \
  --march bernoulli2

# export
hb_mapper makertbin \
  --config config.yaml \
  --model-type onnx
