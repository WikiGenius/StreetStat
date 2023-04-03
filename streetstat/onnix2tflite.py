import tensorflow as tf
from onnx_tf.converter import convert
import os
import argparse

def get_tflite_model(weight, device='CUDA', logging_level='INFO', **kwargs):
    outdir_tf = weight.replace('.onnx', '_tfmodel/')
    if not os.path.isdir(outdir_tf):
        convert(weight, outdir_tf, device=device, logging_level=logging_level, **kwargs)
    
    outfile_tflite = weight.replace('.onnx', '_model.tflite')
    if not os.path.isfile(outfile_tflite):
        converter = tf.lite.TFLiteConverter.from_saved_model(outdir_tf)
        tflite_model = converter.convert()  
        
        with open(outfile_tflite, 'wb') as f:
            f.write(tflite_model)
        print('done converting')
    else:
        print('The file is existed')

    print(outfile_tflite)
    return outfile_tflite

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Process converting ftom ONNIX to TFLITE.')
    parser.add_argument('path_model', type=str, help='Path to the trained ONNIX model file')

    args = parser.parse_args()

    print('Loading: ', args.path_model)

    outfile_tflite = get_tflite_model(weight =  args.path_model)

