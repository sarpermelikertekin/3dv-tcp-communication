import socket
import sys
import cv2
import pickle
import numpy as np
import struct ## new
import zlib
import time
import torch


# receiving the image bytes in chunks
def receive_frame(client_socket, frame_size):
    frame_data = b""
    bytes_received = 0

    print("frame size: ", frame_size)


    while bytes_received < frame_size:
        try:
            chunk = client_socket.recv(min(frame_size - bytes_received, 8388608))
            if not chunk:
                break
            frame_data += chunk
            bytes_received += len(chunk)

        except:
            return frame_data

    return frame_data

#preparing the model output to be usable in Unity side
def prepare_str(objects):
    response = ""
    first = True
    for line in objects.splitlines():
        if first:
            first = False
            continue
        response += line + "; \n"
    return response


def main():
    

    # Create a TCP socket server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip, server_port))
    server_socket.listen(1)

    print('Waiting for client connection...')
    client_socket, address = server_socket.accept()
    print('Client connected:', address)

    while True:
       
        size_data = client_socket.recv(4)
        frame_size = struct.unpack('!I', size_data)[0]

        # Receive the frame from the client
        frame_data = receive_frame(client_socket, frame_size)

        # Process the received frame as needed
        with open(image_path, 'wb') as f:
            f.write(frame_data)

        print('Frame received successfully!')

        #run the yolo model on received frame
        results = model(image_path)
        objects = results.pandas().xyxy[0].to_csv() 
        response = prepare_str(objects)
        #at least send something even if no objects detected
        if(';' not in response):
            response = ";\n"
        
        client_socket.send(response.encode())
    
    
    #maybe put a condition here
    client_socket.close()

    # Close the server socket
    server_socket.close()

server_ip = ''  # listen from any ip
server_port = 5000  
image_path = 'received_frame.jpg'
weights_path = './training results/exp_30052023_1738/weights/best.pt'
model = torch.hub.load('ultralytics/yolov5', 'custom', weights_path)
main()