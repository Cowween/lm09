import numpy as np
import pandas as pd
import keras
import pickle

from pathlib import Path
import os.path

from keras.preprocessing.image import ImageDataGenerator


def prediction(dataset):
    model_path = "EfficientNetB0-525-(224 X 224)- 98.97.h5"
    model = keras.models.load_model(model_path, custom_objects={'F1_score': 'F1_score'})

    image_dir = Path(dataset)

    # Get filepaths and labels
    filepaths = list(image_dir.glob(r'**/*.jpg')) + list(image_dir.glob(r'**/*.png'))
    labels = list(map(lambda x: os.path.split(os.path.split(x)[0])[1], filepaths))

    filepaths = pd.Series(filepaths, name='Filepath').astype(str)
    labels = pd.Series(labels, name='Label')

    # Concatenate filepaths and labels
    image_df = pd.concat([filepaths, labels], axis=1)
    test_generator = ImageDataGenerator(
        preprocessing_function=keras.applications.efficientnet.preprocess_input
    )

    test_images = test_generator.flow_from_dataframe(
        dataframe=image_df,
        x_col="Filepath",
        y_col='Label',
        target_size=(224, 224),
        color_mode='rgb',
        class_mode='categorical',
        batch_size=32,
        shuffle=False
    )

    pred = model.predict(test_images)
    pred = np.argmax(pred, axis=1)

    # Map the label
    with open('labels.pkl', 'rb') as fp:
        labels = pickle.load(fp)
    pred = [labels[k] for k in pred]

    # Display the result
    return pred

