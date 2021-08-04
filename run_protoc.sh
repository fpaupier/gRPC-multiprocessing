#!/bin/bash
set -x # Echo on
python3 -m grpc_tools.protoc --proto_path=./grpc_config --python_out=./grpc_config --grpc_python_out=./grpc_config ./grpc_config/image_ocr.proto
