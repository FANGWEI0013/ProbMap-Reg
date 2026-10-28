import cv2
import numpy as np
from keras.models import load_model

from config import CNN_INPUT_SIZE


def load_unet_model(model_path):
    model = load_model(model_path, compile=False)
    expected_input = (None, CNN_INPUT_SIZE, CNN_INPUT_SIZE, 3)
    expected_output = (None, CNN_INPUT_SIZE, CNN_INPUT_SIZE, 1)
    if model.input_shape != expected_input:
        raise ValueError(f"Unexpected model input shape: {model.input_shape}")
    if model.output_shape != expected_output:
        raise ValueError(f"Unexpected model output shape: {model.output_shape}")
    return model


def read_bgr_image(image_path):
    image = cv2.imread(str(image_path))
    if image is None:
        raise FileNotFoundError(f"Could not read image: {image_path}")
    return image


def preprocess_green_replicated(image_bgr):
    image_resized = cv2.resize(
        src=image_bgr,
        dsize=(CNN_INPUT_SIZE, CNN_INPUT_SIZE),
        interpolation=cv2.INTER_CUBIC,
    )
    _, green, _ = cv2.split(image_resized)
    green_3ch = np.zeros_like(image_resized)
    green_3ch[:, :, 0] = green
    green_3ch[:, :, 1] = green
    green_3ch[:, :, 2] = green
    return green_3ch


def predict_probability_map(model, image_bgr):
    preprocessed = preprocess_green_replicated(image_bgr)
    batch = np.expand_dims(preprocessed, axis=0).astype(np.float32) / 255.0
    prediction = model.predict(batch, verbose=0)
    return prediction[0, :, :, 0]


def predict_pair_probability_maps(model, image_1_bgr, image_2_bgr):
    preprocessed_1 = preprocess_green_replicated(image_1_bgr)
    preprocessed_2 = preprocess_green_replicated(image_2_bgr)
    batch = np.stack([preprocessed_1, preprocessed_2], axis=0).astype(np.float32) / 255.0
    predictions = model.predict(batch, verbose=0)
    return predictions[0, :, :, 0], predictions[1, :, :, 0]
