# Author: Muhammed Elyamani
# Date: 03/02/2023
# GitHub: https://github.com/WikiGenius

import platform

def get_model(model_path, edgetpu = False, num_threads = None):
    
    try:  # https://coral.ai/docs/edgetpu/tflite-python/#update-existing-tf-lite-code-for-the-edge-tpu
        from tflite_runtime.interpreter import Interpreter, load_delegate
    except ImportError:
        import tensorflow as tf
        Interpreter, load_delegate = tf.lite.Interpreter, tf.lite.experimental.load_delegate
    if edgetpu:  # TF Edge TPU https://coral.ai/software/#edgetpu-runtime
        # print(f'Loading {model_path} for TensorFlow Lite Edge TPU inference...')
        delegate = {
            'Linux': 'libedgetpu.so.1',
            'Darwin': 'libedgetpu.1.dylib',
            'Windows': 'edgetpu.dll'}[platform.system()]
        interpreter = Interpreter(model_path=model_path, experimental_delegates=[load_delegate(delegate)], num_threads=num_threads)
    else:  # TFLite
        # print(f'Loading {model_path} for TensorFlow Lite inference...')
        interpreter = Interpreter(model_path=model_path, num_threads=num_threads)  # load TFLite model
    #Allocate tensors.
    interpreter.allocate_tensors()
    # Get input and output tensors.
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    return interpreter, input_details, output_details