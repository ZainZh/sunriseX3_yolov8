#!/bin/bash
# check


hb_mapper checker \
  --model-type onnx \
  --model /home/clover/Downloads/yolov8x.onnx \
  --march bayes\
  --input-shape images 1x3x640x640

