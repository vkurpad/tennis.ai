from keras.utils import Sequence
import keras
import numpy as np
import matplotlib.pyplot as plt

class DataGenerator(Sequence):
    def __init__(self, list_IDs, labels, batch_size=15, dim=(224,224,3), n_channels=3,
             n_classes=2, shuffle=True):
        'Initialization'
        self.dim = dim
        self.batch_size = batch_size
        self.labels = labels
        self.list_IDs = list_IDs
        self.n_channels = n_channels
        self.n_classes = n_classes
        self.shuffle = shuffle
        self.on_epoch_end()
    
    def on_epoch_end(self):
        'Updates indexes after each epoch'
        self.indexes = np.arange(len(self.list_IDs))
        if self.shuffle == True:
            np.random.shuffle(self.indexes)
    
    def __data_generation(self, list_IDs_temp):
        'Generates data containing batch_size samples' # X : (n_samples, *dim, n_channels)
        # Initialization
        x = []
        y = [0] * self.batch_size


        # Generate data
        for i, ID in enumerate(list_IDs_temp):
            # Store sample
            img = plt.imread('static/images/' + ID)
            x.append(img)
            
        
            # Store class
            y[i] = self.labels[i]
        X = np.array(x)
        return X, keras.utils.to_categorical(y, num_classes=self.n_classes)

    def __len__(self):
        'Denotes the number of batches per epoch'
        return int(np.floor(len(self.list_IDs) / self.batch_size))
    

    def __getitem__(self, index):
        'Generate one batch of data'
        # Generate indexes of the batch
        indexes = self.indexes[index*self.batch_size:(index+1)*self.batch_size]

        # Find list of IDs
        list_IDs_temp = [self.list_IDs[k] for k in indexes]

        # Generate data
        X, y = self.__data_generation(list_IDs_temp)

        return X, y


print("Hello")  
params = {'dim': (224,224),
          'batch_size': 15,
          'n_classes': 2,
          'n_channels': 3,
          'shuffle': True}

# Datasets
partition = {'train': ['frame0.jpg', 'frame1.jpg', 'frame3.jpg'], 'validation': ['frame4.jpg']}
labels = [1,0,1,0]

# Generators
training_generator = DataGenerator(partition['train'], labels, **params)
validation_generator = DataGenerator(partition['validation'], labels, **params)

batch = training_generator.__getitem__(0)
print(batch[1])

