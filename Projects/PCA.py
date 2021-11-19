import os
import numpy as np
from numpy import pi, exp, log
from PIL import Image
from numpy import linalg as LA

import sys, os
home_path = os.environ['HOME']
    # Adding the path of the directory with your images to the path
sys.path.append(r'C:\Users\m73ma\OneDrive\Desktop\python')

    # This sets the maximum number of pixes of the image you are importing
Image.MAX_IMAGE_PIXELS = 1000000000


def main():

    # This is the name of the image you want to manipulate
    source_image_filename = '10b.jpg'

    #This is the name of the file you will export
    out_image_filename = '10b_out.jpg'

    # The array will have dimensions (height of image)x(width of image)x(number of channels per pixel)
    # JPEG and GIF images have 3 channels per pixel [red, green, blue]
    # PNG images have either 3 or 4 channels per pixel [red, green, blue, alpha], where the alpha channel sets the opacity of each pixel
    # For most images, each pixel is 8-bit, so its value can be between 0 and 255.
    #Some the images in the FEI database only have 1 channel per pixel. This is code that converts them to a 3-channel RGB image.
#Omar's note: This first loop with if statements is to import pictures, and then does the whole thing the professor explained aboce
    image = np.array(Image.open(source_image_filename),dtype=np.float32)
    image_height = len(image)
    image_width = len(image[0])
    mat=np.zeros([3*image_height*image_width,6])
    k=0
    for k in range(6):
        source_image_filename = str(k)+'.jpg'
        image = np.array(Image.open(source_image_filename),dtype=np.float32)

        image_height = len(image)
        image_width = len(image[0])
        if len(np.shape(image)) == 2:
            img = []
            image_pixels = 3
            for i in range(image_height):
                row = []
                for j in range(image_width):
                    pix = [image[i,j],image[i,j],image[i,j]]
                    row.append(pix)
                img.append(row)
            image = np.array(img)
        elif len(np.shape(image))==3:
            if np.shape(image)[-1] == 3:
                image_pixels = 3
            elif np.shape(image)[-1] == 4:
                image_pixels = 4
        
        mat[:,k]= np.asarray((image).reshape(-1))
# Checking the matrix of rows as data
    print(np.shape(mat))
    mat_height = len(mat)
    mat_width = len(mat[0])
# Attempt at trying out the PCA thingy 
    mean_mat = np.zeros([1,mat_width])
    one_mat = np.ones([mat_height,1])
    for i in range(mat_width):
        mean_mat[:,i]=sum(mat[:,i])/mat_height
    averaged_mat=[]
    averaged_mat=np.matmul(one_mat,mean_mat)
    A_mat=mat-averaged_mat
    co_mat=np.matmul(np.transpose(A_mat),A_mat)
    print(LA.eig(co_mat))
    # this negates an image, i.e. inverts all its colors.
    
    out_image = 255 - image
    # this has the original image at the top and the negated pixels at the bottom and interpolates between them
    out_image = np.empty(shape = (image_height,image_width,image_pixels))
    for i in range(image_height):
        for j in range(image_width):
            for k in range(image_pixels):
                out_image[i][j][k] = (1-2*i/len(image))*image[i][j][k]+i/len(image)*255
    


    Image.fromarray(out_image.astype(np.uint8)).save(out_image_filename)
    print(np.shape(image))
    print("".join(["Image width = ",str(len(mat))]))
    print("".join(["Image length = ",str(len(mat[0]))]))



    return out_image

if __name__ == '__main__':
    main()
