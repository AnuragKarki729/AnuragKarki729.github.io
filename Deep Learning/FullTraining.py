import tensorflow as tf
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D
from keras.callbacks import ModelCheckpoint, EarlyStopping
from keras.utils import image_dataset_from_directory
from keras.src.legacy.preprocessing.image import ImageDataGenerator
import os


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

# Directories for full datasets
train_dir = './TrainTest/Train'
val_dir = './TrainTest/Validation'
test_dir = './TrainTest/Test'

# Image size and batch size
img_height = 150
img_width = 150
batch_size = 32

# Load the full datasets
train_dataset = image_dataset_from_directory(train_dir, image_size=(img_height, img_width), batch_size=batch_size)
val_dataset = image_dataset_from_directory(val_dir, image_size=(img_height, img_width), batch_size=batch_size)
test_dataset = image_dataset_from_directory(test_dir, image_size=(img_height, img_width), batch_size=batch_size)

# Data augmentation
data_augmentation = ImageDataGenerator(
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

# Apply augmentation on the training dataset
train_dataset_augmented = data_augmentation.flow_from_directory(
    train_dir, 
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='sparse'
)

# Convert the augmented dataset to a TensorFlow dataset
augmented_dataset = tf.data.Dataset.from_generator(
    lambda: ((x, tf.cast(y, tf.int32)) for x, y in train_dataset_augmented),
    output_signature=(
        tf.TensorSpec(shape=(None, img_height, img_width, 3), dtype=tf.float32),
        tf.TensorSpec(shape=(None,), dtype=tf.int32)
    )
)

# Combine the original training dataset with the augmented dataset
combined_train_dataset = train_dataset.concatenate(augmented_dataset)

# Shuffle the combined dataset
combined_train_dataset = combined_train_dataset.shuffle(1000).repeat()

# Define the model
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
    Dense(len(train_dataset.class_names), activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

print(model.summary())

# Callbacks for checkpointing and early stopping
checkpoint = ModelCheckpoint(
    'DogPredictionModel.keras',
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

# Train the model using the full datasets
history = model.fit(
    combined_train_dataset,
    validation_data=val_dataset,
    epochs=10,
    steps_per_epoch=len(train_dataset_augmented),
    callbacks=[checkpoint, early_stopping]
)