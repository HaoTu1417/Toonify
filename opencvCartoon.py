
import cv2
import os

def render(img_rgb): 
    if not os.path.isdir(img_rgb):
        print("file not found:", img_rgb)
    else:
        print("file exist")
    img_rgb = cv2.imread(img_rgb) 
    #img_rgb = cv2.resize(img_rgb, (1366,768)) 
    numDownSamples = 2       # number of downscaling steps 
    numBilateralFilters = 50  # number of bilateral filtering steps 

    # -- STEP 1 -- 

    # downsample image using Gaussian pyramid 
    img_color = img_rgb 
    for _ in range(numDownSamples): 
        img_color = cv2.pyrDown(img_color) 
    
    # cv2.imshow("downcolor",img_color) 
    #cv2.waitKey(0) 
    # repeatedly apply small bilateral filter instead of applying 
    # one large filter 
    for _ in range(numBilateralFilters): 
        img_color = cv2.bilateralFilter(img_color, 9, 9, 7) 

    # cv2.imshow("bilateral filter",img_color) 
    #cv2.waitKey(0) 
    # upsample image to original size 
    for _ in range(numDownSamples): 
        img_color = cv2.pyrUp(img_color) 
    # cv2.imshow("upscaling",img_color) 
    #cv2.waitKey(0) 

    # -- STEPS 2 and 3 -- 
    # convert to grayscale and apply median blur 
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY) 
    img_blur = cv2.medianBlur(img_gray, 3) 
    # cv2.imshow("grayscale+median blur",img_color) 
    #cv2.waitKey(0) 

    # -- STEP 4 -- 
    # detect and enhance edges 
    img_edge = cv2.adaptiveThreshold(img_blur, 255, 
                                        cv2.ADAPTIVE_THRESH_MEAN_C, 
                                        cv2.THRESH_BINARY, 9, 2) 
    # cv2.imshow("edge",img_edge) 
    #cv2.waitKey(0) 

    # -- STEP 5 -- 
    # convert back to color so that it can be bit-ANDed with color image 
    (x,y,z) = img_color.shape 
    img_edge = cv2.resize(img_edge,(y,x))  
    img_edge = cv2.cvtColor(img_edge, cv2.COLOR_GRAY2RGB) 
    # cv2.imwrite("edge.png",img_edge) 
    # cv2.imshow("step 5", img_edge) 
    #cv2.waitKey(0) 
    #img_edge = cv2.resize(img_edge,(i for i in img_color.shape[:2])) 
    #print img_edge.shape, img_color.shape 
    return cv2.bitwise_and(img_color, img_edge) 
    # return img_edge
  
def cartoonify(file_name):    
    img_rgb = cv2.imread(file_name)
    numBilateralFilters = 3

    img_color = img_rgb

    for i in range(numBilateralFilters):

      img_color = cv2.bilateralFilter(img_color, 15, 30, 20)

      #cv2.imshow(str.format("name{0}",i),img_color)

    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

    img_blur = cv2.medianBlur(img_gray, 7)

    #cv2.imshow("name",img_blur)

    img_edge = cv2.adaptiveThreshold(img_blur, 2,cv2.ADAPTIVE_THRESH_MEAN_C,

    cv2.THRESH_BINARY, 3, 2)

    #cv2.imshow("img_edge",img_edge)
    #cv2.imshow("img_color",img_color)
    img_edge = cv2.cvtColor(img_edge, cv2.COLOR_GRAY2RGB)
    #cv2.imshow("img_edge2",img_edge) 
    #return cv2.bitwise_and(img_color, img_edge)
    return img_color

# tmp_canvas = PencilCartoonizer() 
  
file_name = "image.jpg" #File_name will come here 
# ok
res = render(file_name) 
output = cartoonify(file_name)
cv2.imshow("Cartoon version", output) 
cv2.imshow("Cartoon version 2", res) 
cv2.waitKey(0) 
cv2.destroyAllWindows()
# real_inputs.append(img_rgb)

# cartoon_outputs.append(output)