#!/bin/bash
# check


hb_mapper checker \
  --model-type onnx \
  --model /home/clover/ultralytics/runs/detect/train7/weights/best.onnx \
  --march bayes\
  --input-shape images 1x3x640x640

