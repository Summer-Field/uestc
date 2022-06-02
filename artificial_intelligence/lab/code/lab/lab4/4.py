# 导包
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical
from tensorflow import keras
import matplotlib.pyplot as plt

# 装载数据集
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()

print("test_images.shape: ", test_images.shape)

# 数据处理
train_images = train_images.reshape((60000, 28, 28, 1))
train_images = train_images.astype('float') / 255

test_images = test_images.reshape((10000, 28, 28, 1))
test_images = test_images.astype('float') / 255

train_labels = to_categorical(train_labels)
test_labels = to_categorical(test_labels)

print("train_labels.shape: ", train_labels.shape)

# 搭建模型
model = keras.models.Sequential([
    keras.layers.Conv2D(32, (3, 3), activation='relu',
                        input_shape=(28, 28, 1)),
    keras.layers.MaxPooling2D((2, 2)),
    keras.layers.Conv2D(64, (3, 3), activation='relu'),
    keras.layers.MaxPooling2D((2, 2)),
    keras.layers.Conv2D(64, (3, 3), activation='relu'),
    keras.layers.MaxPooling2D((2, 2)),
    keras.layers.Flatten(),
    keras.layers.Dense(64, activation='relu'),
    keras.layers.Dense(10, activation='softmax')
])

# 模型编译与训练
model.compile(optimizer=keras.optimizers.Adam(),
              loss='categorical_crossentropy',
              metrics=['accuracy'])
model.summary()
history = model.fit(train_images, train_labels, epochs=10, batch_size=64)

# 数据可视化
accuracy = history.history['accuracy']
loss = history.history['loss']

plt.subplot(1, 2, 1)
plt.plot(accuracy, label='Training Loss')
plt.title('Training Accuracy')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(loss, label='Training Loss')
plt.title('Traiining Loss')
plt.legend()
plt.show()