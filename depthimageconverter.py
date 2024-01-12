# -*- coding: utf-8 -*-
"""DepthImageConverter.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1voqZ1c-iH9sF_SuidZisSRnrqSNQuEmA
"""

!pip install torch torchvision timm opencv-python

import torch
from torchvision import transforms
from PIL import Image
import cv2
import matplotlib.pyplot as plt
from google.colab import files

# Load MiDaS model
class MidasNet(torch.nn.Module):
    def __init__(self, path=None, device='cpu'):
        super(MidasNet, self).__init__()

        # Load the MiDaS model
        self.model = torch.hub.load('intel-isl/MiDaS', 'MiDaS')
        self.device = device

        if path is not None:
            checkpoint = torch.load(path, map_location=torch.device(device))
            self.load_adjusted_state_dict(checkpoint)

    def load_adjusted_state_dict(self, state_dict):
        model_state_dict = self.model.state_dict()
        adjusted_state_dict = {}
        for k, v in state_dict.items():
            if k.startswith('model.'):
                k = k[len('model.'):]
            if k in model_state_dict:
                adjusted_state_dict[k] = v

        self.model.load_state_dict(adjusted_state_dict)

    def forward(self, x):
        return self.model(x)

# Download the MiDaS model
device = 'cuda' if torch.cuda.is_available() else 'cpu'
midas_model = MidasNet(device=device)
model_url = "https://github.com/isl-org/MiDaS/releases/download/v2_1/midas_v21_384.pt"
checkpoint = torch.hub.load_state_dict_from_url(model_url, map_location=torch.device(device))
midas_model.load_adjusted_state_dict(checkpoint)

# Upload an image file to Colab
uploaded = files.upload()
image_path = list(uploaded.keys())[0]

# Load the uploaded image
img = Image.open(image_path)

# Preprocess the image
transform = transforms.Compose([
    transforms.Resize((384, 384)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

input_img = transform(img).unsqueeze(0)

# Move the model to the appropriate device
midas_model.to(device)
input_img = input_img.to(device)

# Run MiDaS on the image
with torch.no_grad():
    prediction = midas_model(input_img)

# Display the input image and depth map
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.imshow(img)
plt.title('Input Image')

plt.subplot(1, 2, 2)
plt.imshow(prediction.squeeze().cpu(), cmap='viridis')
plt.title('Depth Map')

plt.show()

import torch
from torchvision import transforms
from PIL import Image
import cv2
import matplotlib.pyplot as plt
from google.colab import files

class MidasNet(torch.nn.Module):
    def __init__(self, path=None, device='cpu'):
        super(MidasNet, self).__init__()

        self.model = torch.hub.load('intel-isl/MiDaS', 'MiDaS')
        self.device = device

        if path is not None:
            checkpoint = torch.load(path, map_location=torch.device(device))
            self.load_adjusted_state_dict(checkpoint)

    def load_adjusted_state_dict(self, state_dict):
        model_state_dict = self.model.state_dict()
        adjusted_state_dict = {}
        for k, v in state_dict.items():
            if k.startswith('model.'):
                k = k[len('model.'):]
            if k in model_state_dict:
                adjusted_state_dict[k] = v

        self.model.load_state_dict(adjusted_state_dict)

    def forward(self, x):
        return self.model(x)

def convert_to_black_and_white(image_path):
    img = Image.open(image_path).convert('L')  # Convert to black and white
    img = img.convert('RGB')  # Convert to 3-channel grayscale
    return img

def estimate_depth_and_distance(image_path, midas_model, device='cuda'):
    # Preprocess the image
    transform = transforms.Compose([
        transforms.Resize((384, 384)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    img = Image.open(image_path)
    img_bw = convert_to_black_and_white(image_path)
    input_img = transform(img_bw).unsqueeze(0)

    # Move the model to the appropriate device
    midas_model.to(device)
    input_img = input_img.to(device)

    # Run MiDaS on the image
    with torch.no_grad():
        prediction = midas_model(input_img)

    # Display the input image, black and white image, and depth map
    plt.figure(figsize=(15, 5))

    plt.subplot(1, 3, 1)
    plt.imshow(img)
    plt.title('Original Image')

    plt.subplot(1, 3, 2)
    plt.imshow(img_bw, cmap='gray')
    plt.title('Black and White Image')

    plt.subplot(1, 3, 3)
    plt.imshow(prediction.squeeze().cpu(), cmap='viridis')
    plt.title('Depth Map')

    plt.show()

    # Calculate the distance between two points (e.g., two objects in the image)
    # For simplicity, we'll assume you know the coordinates of the two points in pixel space
    point1 = (100, 150)  # Example coordinates (replace with actual coordinates)
    point2 = (200, 250)  # Example coordinates (replace with actual coordinates)

    depth_point1 = prediction[0, point1[1], point1[0]].item()
    depth_point2 = prediction[0, point2[1], point2[0]].item()

    # Assuming a simple linear relationship between depth and distance
    distance_factor = 0.1  # You may need to adjust this factor based on your specific scenario
    distance1 = depth_point1 * distance_factor
    distance2 = depth_point2 * distance_factor

    distance_between_objects = abs(distance2 - distance1)

    return distance_between_objects

# Upload an image file to Colab
uploaded = files.upload()
image_path = list(uploaded.keys())[0]

# Download the MiDaS model
device = 'cuda' if torch.cuda.is_available() else 'cpu'
model_url = "https://github.com/isl-org/MiDaS/releases/download/v2_1/midas_v21_384.pt"
checkpoint = torch.hub.load_state_dict_from_url(model_url, map_location=torch.device(device))

midas_model = MidasNet(device=device)
midas_model.load_adjusted_state_dict(checkpoint)

# Estimate depth and distance
distance_between_objects = estimate_depth_and_distance(image_path, midas_model, device=device)
print(f"Estimated distance between objects: {distance_between_objects} meters")

import torch
from torchvision import transforms
from PIL import Image
import cv2
import matplotlib.pyplot as plt
from google.colab import files

class MidasNet(torch.nn.Module):
    def __init__(self, path=None, device='cpu'):
        super(MidasNet, self).__init__()

        self.model = torch.hub.load('intel-isl/MiDaS', 'MiDaS')
        self.device = device

        if path is not None:
            checkpoint = torch.load(path, map_location=torch.device(device))
            self.load_adjusted_state_dict(checkpoint)

    def load_adjusted_state_dict(self, state_dict):
        model_state_dict = self.model.state_dict()
        adjusted_state_dict = {}
        for k, v in state_dict.items():
            if k.startswith('model.'):
                k = k[len('model.'):]
            if k in model_state_dict:
                adjusted_state_dict[k] = v

        self.model.load_state_dict(adjusted_state_dict)

    def forward(self, x):
        return self.model(x)

def convert_to_black_and_white(image_path):
    img = Image.open(image_path).convert('L')  # Convert to black and white
    img = img.convert('RGB')  # Convert to 3-channel grayscale
    return img

def estimate_depth_and_distance(image_path, midas_model, device='cuda'):
    # Preprocess the image
    transform = transforms.Compose([
        transforms.Resize((384, 384)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    img = Image.open(image_path)
    img_bw = convert_to_black_and_white(image_path)
    input_img = transform(img_bw).unsqueeze(0)

    # Move the model to the appropriate device
    midas_model.to(device)
    input_img = input_img.to(device)

    # Run MiDaS on the image
    with torch.no_grad():
        prediction = midas_model(input_img)

    # Display the input image, black and white image, and depth map
    plt.figure(figsize=(15, 5))

    plt.subplot(1, 3, 1)
    plt.imshow(img)
    plt.title('Original Image')

    plt.subplot(1, 3, 2)
    plt.imshow(img_bw, cmap='gray')
    plt.title('Black and White Image')

    plt.subplot(1, 3, 3)
    depth_map = prediction.squeeze().cpu()
    plt.imshow(depth_map, cmap='viridis')
    plt.title('Depth Map')

    # Calculate the distance between two points (e.g., two objects in the image)
    # For simplicity, we'll assume you know the coordinates of the two points in pixel space
    point1 = (100, 150)  # Example coordinates (replace with actual coordinates)
    point2 = (200, 250)  # Example coordinates (replace with actual coordinates)

    depth_point1 = depth_map[point1[1], point1[0]].item()
    depth_point2 = depth_map[point2[1], point2[0]].item()

    # Assuming a simple linear relationship between depth and distance
    distance_factor = 0.1  # You may need to adjust this factor based on your specific scenario
    distance1 = depth_point1 * distance_factor
    distance2 = depth_point2 * distance_factor

    distance_between_objects = abs(distance2 - distance1)

    # Plot depth chart
    plt.figure(figsize=(8, 5))
    plt.plot(depth_map[point1[1]:point2[1], point1[0]:point2[0]].cpu().numpy().flatten(), label='Depth values')
    plt.xlabel('Pixel Index')
    plt.ylabel('Depth (Normalized)')
    plt.title('Depth Chart between Selected Points')
    plt.legend()
    plt.show()

    return distance_between_objects

# Upload an image file to Colab
uploaded = files.upload()
image_path = list(uploaded.keys())[0]

# Download the MiDaS model
device = 'cuda' if torch.cuda.is_available() else 'cpu'
model_url = "https://github.com/isl-org/MiDaS/releases/download/v2_1/midas_v21_384.pt"
checkpoint = torch.hub.load_state_dict_from_url(model_url, map_location=torch.device(device))

midas_model = MidasNet(device=device)
midas_model.load_adjusted_state_dict(checkpoint)

# Estimate depth and distance
distance_between_objects = estimate_depth_and_distance(image_path, midas_model, device=device)
print(f"Estimated distance between objects: {distance_between_objects} meters")

import torch
from torchvision import transforms
from PIL import Image
import cv2
import matplotlib.pyplot as plt
from google.colab import files

class MidasNet(torch.nn.Module):
    def __init__(self, path=None, device='cpu'):
        super(MidasNet, self).__init__()

        self.model = torch.hub.load('intel-isl/MiDaS', 'MiDaS')
        self.device = device

        if path is not None:
            checkpoint = torch.load(path, map_location=torch.device(device))
            self.load_adjusted_state_dict(checkpoint)

    def load_adjusted_state_dict(self, state_dict):
        model_state_dict = self.model.state_dict()
        adjusted_state_dict = {}
        for k, v in state_dict.items():
            if k.startswith('model.'):
                k = k[len('model.'):]
            if k in model_state_dict:
                adjusted_state_dict[k] = v

        self.model.load_state_dict(adjusted_state_dict)

    def forward(self, x):
        return self.model(x)

def convert_to_black_and_white(image_path):
    img = Image.open(image_path).convert('L')  # Convert to black and white
    img = img.convert('RGB')  # Convert to 3-channel grayscale
    return img

def estimate_depth_and_distance(image_path, midas_model, device='cuda'):
    # Preprocess the image
    transform = transforms.Compose([
        transforms.Resize((384, 384)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    img = Image.open(image_path)
    img_bw = convert_to_black_and_white(image_path)
    input_img = transform(img_bw).unsqueeze(0)

    # Move the model to the appropriate device
    midas_model.to(device)
    input_img = input_img.to(device)

    # Run MiDaS on the image
    with torch.no_grad():
        prediction = midas_model(input_img)

    # Display the input image, black and white image, and depth map
    plt.figure(figsize=(15, 5))

    plt.subplot(1, 3, 1)
    plt.imshow(img)
    plt.title('Original Image')

    plt.subplot(1, 3, 2)
    plt.imshow(img_bw, cmap='gray')
    plt.title('Black and White Image')

    plt.subplot(1, 3, 3)
    depth_map = prediction.squeeze().cpu()
    plt.imshow(depth_map, cmap='viridis')
    plt.title('Depth Map')

    # Calculate the distance between two points (e.g., two objects in the image)
    # For simplicity, we'll assume you know the coordinates of the two points in pixel space
    point1 = (100, 150)  # Example coordinates (replace with actual coordinates)
    point2 = (200, 250)  # Example coordinates (replace with actual coordinates)

    depth_point1 = depth_map[point1[1], point1[0]].item()
    depth_point2 = depth_map[point2[1], point2[0]].item()

    # Assuming a simple linear relationship between depth and distance
    distance_factor = 0.1  # You may need to adjust this factor based on your specific scenario
    distance1 = depth_point1 * distance_factor
    distance2 = depth_point2 * distance_factor

    distance_between_objects = abs(distance2 - distance1)

    # Plot color chart
    plt.figure(figsize=(8, 5))
    color_values = img.getpixel((point1[0], point1[1]))
    plt.plot(color_values, label='Color values')
    plt.xlabel('Channel Index')
    plt.ylabel('Color Value')
    plt.title('Color Chart at Selected Point')
    plt.legend()
    plt.show()

    return distance_between_objects

# Upload an image file to Colab
uploaded = files.upload()
image_path = list(uploaded.keys())[0]

# Download the MiDaS model
device = 'cuda' if torch.cuda.is_available() else 'cpu'
model_url = "https://github.com/isl-org/MiDaS/releases/download/v2_1/midas_v21_384.pt"
checkpoint = torch.hub.load_state_dict_from_url(model_url, map_location=torch.device(device))

midas_model = MidasNet(device=device)
midas_model.load_adjusted_state_dict(checkpoint)

# Estimate depth and distance
distance_between_objects = estimate_depth_and_distance(image_path, midas_model, device=device)
print(f"Estimated distance between objects: {distance_between_objects} meters")