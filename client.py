# Python std lib
import time
import os
import atexit
import multiprocessing
import typing as tp
import pickle
import sys

# 3rd party libs
import cv2 as cv
import grpc
from simber import Logger

# Local grpc module
sys.path.append("/usr/app/grpc_config")
import image_ocr_pb2
import image_ocr_pb2_grpc

LOG_FORMAT = "{levelname} [{filename}:{lineno}]:"

LOG_LEVEL: str = "INFO"
logger = Logger(__name__, log_path="/tmp/logs/server.log", level=LOG_LEVEL)
logger.update_format(LOG_FORMAT)

NUM_WORKERS = int(os.environ.get("NUM_WORKERS", 2))
NUM_IMAGES = int(os.environ.get("NUM_IMAGES", 40))

_worker_channel_singleton = None
_worker_stub_singleton = None


def _shutdown_worker():
    """
    Close the open gRPC channel.

    Returns:
        None

    """
    if _worker_channel_singleton is not None:
        _worker_channel_singleton.stop()


def _initialize_worker(server_address: str) -> None:
    """
    Setup a grpc stub if not available.

    Args:
        server_address (str)

    Returns:
        None
    """
    global _worker_channel_singleton
    global _worker_stub_singleton
    _worker_channel_singleton = grpc.insecure_channel(
        server_address,
        options=[
            ("grpc.max_send_message_length", -1),
            ("grpc.max_receive_message_length", -1),
            ("grpc.so_reuseport", 1),
            ("grpc.use_local_subchannel_pool", 1),
        ], )
    _worker_stub_singleton = image_ocr_pb2_grpc.OCRStub(_worker_channel_singleton)
    atexit.register(_shutdown_worker)


def _run_worker_query(img: bytes) -> str:
    """
    Execute the call to the gRPC server.

    Args:
        img (bytes): bytes representation of the image

    Returns:
        detected text on the image

    """
    logger.info("_run_worker_query(): Entering")
    response: image_ocr_pb2.OcrResult = _worker_stub_singleton.Detect(
        image_ocr_pb2.OcrCandidate(image=img)
    )
    logger.info(f"_run_worker_query(): exiting: {response.text}")
    return response.text


def compute_detections(batch: tp.List[bytes]) -> tp.List[str]:
    """
    Start a pool of process to parallelize data processing across several workers.

    Args:
        batch: a list of images.

    Returns:
        the list of detected texts.

    Inspired from https://github.com/grpc/grpc/blob/master/examples/python/multiprocessing/client.py

    """
    server_address = 'server:13000'
    logger.info("compute_detections(): Entering")
    with multiprocessing.Pool(processes=NUM_WORKERS,
                              initializer=_initialize_worker,
                              initargs=(server_address,),
                              ) as worker_pool:
        logger.info("compute_detections(): In the with context")
        ocr_results = worker_pool.map(_run_worker_query, [pickle.dumps(img) for img in batch])
        return [txt for txt in ocr_results]


def prepare_batch() -> tp.List[bytes]:
    """
    Generate a batch of image data to process.

    Returns:
        batch: (tp.List[bytes])
    """
    logger.info('Reading src image...')
    source = "/usr/app/motivational_quote.jpg"
    img = cv.imread(source)
    batch: tp.List[bytes] = []
    for _ in range(NUM_IMAGES):
        batch.append(img)
    # FIll last batch with remaining
    return batch


def run():
    logger.info('OCR Test client started!')
    batch = prepare_batch()
    logger.info('Batch ready, calling grpc server...')

    start = time.perf_counter()
    results = compute_detections(batch)
    duration = time.perf_counter() - start

    logger.info(f'gRPC server answered. Processed {NUM_IMAGES} images in {duration} UA ({NUM_WORKERS} workers)')
    logger.info(f"Text  detected on the first image: {results[0]}")


if __name__ == "__main__":
    run()
