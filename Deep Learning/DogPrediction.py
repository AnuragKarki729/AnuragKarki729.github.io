import tensorflow as tf
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense 
from keras.layers import Dropout
from keras.layers import Flatten
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.callbacks import ModelCheckpoint, EarlyStopping
from keras import backend as K
from keras.utils import image_dataset_from_directory
import shutil
import os


subset_val_dir = './TrainTest/ValidationSubset'
os.makedirs(subset_val_dir, exist_ok=True)

subset_test_dir = './TrainTest/TestSubset'
os.makedirs(subset_test_dir, exist_ok=True)

# dataset = './Images'
# output = './TrainTest'

# train_dir = os.path.join(output, 'Train')
# val_dir = os.path.join(output, 'Validation')
# test_dir = os.path.join(output, 'Test')

# os.makedirs(train_dir, exist_ok=True)
# os.makedirs(val_dir, exist_ok=True)
# os.makedirs(test_dir, exist_ok=True)

# breed_dirs = [f for f in os.listdir(dataset) if os.path.isdir(os.path.join(dataset, f))]

# # Set your desired split ratios
# train_ratio = 0.7
# val_ratio = 0.15
# test_ratio = 0.15

# for breed in breed_dirs:
#     breed_path = os.path.join(dataset, breed)
    
#     # Create breed subdirectories in Train, Validation, Test
#     os.makedirs(os.path.join(train_dir, breed), exist_ok=True)
#     os.makedirs(os.path.join(val_dir, breed), exist_ok=True)
#     os.makedirs(os.path.join(test_dir, breed), exist_ok=True)
    
#     # List all images for the breed
#     images = os.listdir(breed_path)
    
#     # Shuffle images and split them
#     train_images, temp_images = train_test_split(images, test_size=(1 - train_ratio), random_state=42)
#     val_images, test_images = train_test_split(temp_images, test_size=(test_ratio / (test_ratio + val_ratio)), random_state=42)
    
#     # Move the images to their respective directories
#     for image in train_images:
#         shutil.move(os.path.join(breed_path, image), os.path.join(train_dir, breed, image))
    
#     for image in val_images:
#         shutil.move(os.path.join(breed_path, image), os.path.join(val_dir, breed, image))
    
#     for image in test_images:
#         shutil.move(os.path.join(breed_path, image), os.path.join(test_dir, breed, image))

# print("Dataset split into training, validation, and test sets.")

train_dir = './TrainTest/Train'
val_dir = './TrainTest/Validation'
test_dir = './TrainTest/Test'

original_train_dir = './TrainTest/Train'
subset_train_dir = './TrainTest/TrainSubset'
os.makedirs(subset_train_dir, exist_ok=True)


breed_dirs = [f for f in os.listdir(original_train_dir) if os.path.isdir(os.path.join(original_train_dir, f))]
import random
for breed in breed_dirs:
    os.makedirs(os.path.join(subset_train_dir, breed), exist_ok=True)
    
    # Get all images for the breed
    breed_path = os.path.join(train_dir, breed)
    images = os.listdir(breed_path)
    
    # Randomly select 5 images
    selected_images = random.sample(images, min(5, len(images)))
    
    # Copy the selected images to the subset directory
    for image in selected_images:
        shutil.copy(os.path.join(breed_path, image), os.path.join(subset_train_dir, breed, image))

print("Subset of images created.")

test_breed_dirs = [f for f in os.listdir(test_dir) if os.path.isdir(os.path.join(test_dir, f))]

# For each breed, copy 5 images to the validation subset directory
for breed in test_breed_dirs:
    os.makedirs(os.path.join(subset_val_dir, breed), exist_ok=True)
    
    # Get all images for the breed in the validation set
    breed_path = os.path.join(test_dir, breed)
    images = os.listdir(breed_path)
    
    # Randomly select 5 images
    selected_images = random.sample(images, min(5, len(images)))
    
    # Copy the selected images to the validation subset directory
    for image in selected_images:
        shutil.copy(os.path.join(breed_path, image), os.path.join(subset_val_dir, breed, image))

print("Validation subset of images created.")

val_breed_dirs = [f for f in os.listdir(val_dir) if os.path.isdir(os.path.join(val_dir, f))]

# For each breed, copy 5 images to the validation subset directory
for breed in val_breed_dirs:
    os.makedirs(os.path.join(subset_test_dir, breed), exist_ok=True)
    
    # Get all images for the breed in the validation set
    breed_path = os.path.join(val_dir, breed)
    images = os.listdir(breed_path)
    
    # Randomly select 5 images
    selected_images = random.sample(images, min(5, len(images)))
    
    # Copy the selected images to the validation subset directory
    for image in selected_images:
        shutil.copy(os.path.join(breed_path, image), os.path.join(subset_test_dir, breed, image))

print("Validation subset of Test images created.")


batch_size = 32
img_height = 150
img_width = 150

train_dataset = image_dataset_from_directory(train_dir, image_size=(img_height, img_width), batch_size=batch_size)

val_dataset = image_dataset_from_directory(val_dir, image_size=(img_height, img_width), batch_size=batch_size)

test_dataset = image_dataset_from_directory(test_dir, image_size=(img_height, img_width), batch_size=batch_size)

train_subset_dataset = image_dataset_from_directory(subset_train_dir, image_size=(img_height, img_width), batch_size=batch_size)

val_subset_dataset = image_dataset_from_directory(subset_val_dir, image_size=(img_height, img_width), batch_size=batch_size)

model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(img_height, img_width, 3), padding='same'),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu', padding='same'),
    MaxPooling2D((2, 2)),
    Conv2D(128, (3, 3), activation='relu', padding='same'),
    MaxPooling2D((2, 2)),
    Conv2D(256, (3, 3), activation='relu', padding='same'),  
    MaxPooling2D((2, 2)),
    Conv2D(512, (3, 3), activation='relu', padding='same'), 
    MaxPooling2D((2, 2)),
    Flatten(),
    Dense(512, activation='relu'),
    Dropout(0.5),
    Dense(len(train_subset_dataset.class_names), activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

print(model.summary())

checkpoint = ModelCheckpoint(
    'DogPredictionModel.keras',  # Path where the model will be saved
    monitor='val_accuracy',  
    save_best_only=True,  
    mode='max',  
    verbose=1  
)


early_stopping = EarlyStopping(
    monitor='val_loss', 
    patience=10,  
    restore_best_weights=False,  
    mode='min', 
    verbose=1  
)

history = model.fit(
    train_subset_dataset,
    validation_data=val_subset_dataset,  
    epochs=10,
    callbacks=[checkpoint, early_stopping]
)