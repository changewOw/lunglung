import keras
# import tensorflow as tf
from keras.applications.resnet50 import ResNet50
from keras.layers import *
from keras.metrics import categorical_accuracy
import keras.backend as K


def create_model(num_classes):
    input_image = Input(shape=(448, 448, 3), name='input_image')
    base_model = ResNet50(include_top=False, input_tensor=input_image, weights='imagenet', pooling=None)
    x = base_model.get_layer('activation_49').output

    mask = Conv2D(1, kernel_size=1, padding='valid', use_bias=True, name='mask')(x)
    mask = AvgPool2D(pool_size=(2, 2), strides=2)(mask)
    mask = Activation(activation='tanh')(mask)
    mask = Reshape((49,), name='loc')(mask)

    x = AvgPool2D(pool_size=(14, 14))(x)
    x = Reshape((2048,))(x)

    out1 = Dense(num_classes, use_bias=False, name='cls')(x)
    out2 = Dense(2, use_bias=False, name='adv')(x)

    return keras.models.Model(input_image, [out1, out2, mask], name='dcl')

if __name__ == '__main__':
    base_model = create_model(2)
    base_model.summary()