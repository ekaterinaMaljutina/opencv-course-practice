import cv2 as cv
import sys
from matplotlib import pyplot as plt


def average(img,dist):
	ratio=1
	rows,cols = img.shape	
	max_dist =int (dist.max())
	img_new = img.copy()
	integral_img=cv.integral(img)
	for i in range(0,rows):
		for j in range(0,cols):
			kernel = int (dist[i][j]*ratio) 
			if kernel % 2 == 0: kernel+=1
			if kernel>1:
				max_x=max(0,i-kernel/2)
				min_y=min(cols-1,j+kernel/2)
				min_x = min(rows-1,i+kernel/2)
				max_y= max(0,j-kernel/2)

				A = integral_img[max_x+1,max_y+1]
				B = integral_img[min_x, max_y+1]
				C = integral_img[max_x+1, min_y]
				D = integral_img[min_x,min_y]
				mean = A+D-C-B
				mean = mean/(max_x - min_x+1)/(max_y- min_y+1)
				img_new[i][j]=mean
			else:
				img_new[i][j] = img[i][j]

	return img_new


			

if __name__ == '__main__':
    if (len(sys.argv)==2):
    	plt.subplot(2,3,1)
        img = cv.imread(sys.argv[1]) 
        copy_img = img.copy()
        plt.imshow(copy_img)
        plt.xticks([]), plt.yticks([])
        plt.title('img')
        print img.shape
        img_gray = cv.cvtColor(img,cv.COLOR_RGB2GRAY)
        plt.subplot(2,3,2)
        plt.imshow(img_gray, cmap = 'gray')
        plt.xticks([]), plt.yticks([])
        plt.title('img_gray')
        if (img_gray == None):
            print "image is empty"
        else: 
			laplacian = cv.Laplacian(img_gray,cv.CV_64F)
			sobelx = cv.Sobel(img_gray,cv.CV_64F,1,0,ksize=3)
			sobely = cv.Sobel(img_gray,cv.CV_64F,0,1,ksize=3)

			plt.subplot(2,3,3)
			plt.imshow(laplacian,cmap = 'gray')
			plt.xticks([]), plt.yticks([])
			plt.title('Laplacian')


			edges = cv.Canny(img_gray,100,200)
			edges = 255 - edges
			plt.subplot(2,3,3)
			plt.imshow(edges,cmap = 'gray')
			plt.xticks([]), plt.yticks([])
			plt.title('edges')				
			dist = cv.distanceTransform(edges,cv.cv.CV_DIST_L2,3)
			#cv.normalize(dist,dist,0,1,cv.NORM_MINMAX) 
			plt.subplot(2,3,4)
			plt.xticks([]), plt.yticks([])
			plt.imshow(dist*0.5,cmap = 'gray')
			plt.title('dist')
			r,g,b = cv.split(img)
			r=average(r,dist)
			g=average(g,dist)
			b=average(b,dist)
			new_image=cv.merge((r,g,b))
			
			

			
			plt.subplot(2,3,5)
			plt.xticks([]), plt.yticks([])
			plt.imshow(new_image)
			plt.title('img_average ')
			plt.show()
			'''cv.imshow("img_average", new_image)	
			cv.imshow("img", img)	
			cv.waitKey()'''
                   