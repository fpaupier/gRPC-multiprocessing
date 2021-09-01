# gRPC-multiprocessing

_A boilerplate to use multiprocessing for your gRPC server in your Python project_ 

This repo is a boilerplate showing how you can use **multiprocessing** with gRPC in python.

## Getting started

This project offers a minimum reproducible example of clients sending batches of images to gRPC servers.

The `client.py` starts a pool of several gRPC channel. Each of those clients process send a batch to one of the gRPC server
in parallel.

Copy the `.env.example` file into a `.env` file, adjust the `NUM_IMAGES` and `NUM_WORKERS` variables 
and start playing around by typing  

```bash
git clone git@github.com:fpaupier/gRPC-multiprocessing.git && cd gRPC-multiprocessing

cp .env.example .env  # adjust the nº of workers as you wish
docker-compose run client
# INFO [/usr/app/client.py:126]: OCR Test client started. 
# INFO [/usr/app/client.py:115]: Reading src image...
# ...
```

## Curated resources

on the Internet

- This repo strongly builds on top of Google example on how to use gRPC for multiprocessing.
  https://github.com/grpc/grpc/blob/master/examples/python/multiprocessing

-----

Project social image credits to [Miguel Á. Padriñán](https://www.pexels.com/@padrinan)
