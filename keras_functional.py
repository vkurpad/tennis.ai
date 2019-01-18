
# How to use the functional API in Keras
# https://machinelearningmastery.com/keras-functional-api-deep-learning/

from tensorflow.keras.models import Model
from tensorflow.keras.layers import * 
from tensorflow.keras.utils import plot_model

# Arm 1
visible_1 = Input(shape=(64,64,3), name="in_1")
conv_a_1 = Conv2D(32, kernel_size=4, activation="relu")(visible_1)
pool_a_1 = MaxPooling2D(pool_size=(2,2))(conv_a_1)
flat_a_1 = Flatten()(pool_a_1)

# Arm 2
visible_2 = Input(shape=(64,64,3), name="in_2")
conv_a_2 = Conv2D(32, kernel_size=4, activation="relu")(visible_2)
pool_a_2 = MaxPooling2D(pool_size=(2,2))(conv_a_2)
flat_a_2 = Flatten()(pool_a_2)

# Arm 3
visible_3 = Input(shape=(64,64,3), name="in_3")
conv_a_3 = Conv2D(32, kernel_size=4, activation="relu")(visible_3)
pool_a_3 = MaxPooling2D(pool_size=(2,2))(conv_a_3)
flat_a_3 = Flatten()(pool_a_3)



# concated layers
merged_layers = concatenate([flat_a_1, flat_a_2, flat_a_3])
hidden_1 = Dense(10, activation="relu")(merged_layers)
output = Dense(1, activation="sigmoid")(hidden_1)
model = Model(inputs=[visible_1, visible_2, visible_3], outputs=output)

print(model.summary())

plot_model(model, to_file='shared_input_layer.png')