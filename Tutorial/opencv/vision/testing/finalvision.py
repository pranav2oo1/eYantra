        #image processing differentiate btw red and ble
        #input to arduino
        #area of contour
import cv2
import numpy as np
import serial
import time
import requests


def nothing(int):
            #any operation
    pass
var=0
            #   input
url="http://172.17.55.153:8080/shot.jpg"
ser=serial.Serial('COM4',9800)



while True:
            img_resp=requests.get(url)
            img_arr=np.array(bytearray(img_resp.content),dtype=np.uint8)
            frame=cv2.imdecode(img_arr,-1)
            rows,cols,channels=frame.shape
            #calibrations
            # get current positions of the trackbars
            #red_ilowH = cv2.getTrackbarPos('lowH', 'red')
            red_ilowH=110
            #red_ihighH = cv2.getTrackbarPos('highH', 'red')
            red_ihighH=130
            #red_ilowS = cv2.getTrackbarPos('lowS', 'red')
            red_ilowS=50
            #red_ihighS = cv2.getTrackbarPos('highS', 'red')
            red_ihighS=255
            #red_ilowV = cv2.getTrackbarPos('lowV', 'red')
            red_ilowV=50
            #red_ihighV = cv2.getTrackbarPos('highV', 'red')
            red_ihighH=255
            # get current positions of the trackbars
            #blue_ilowH = cv2.getTrackbarPos('lowH', 'blue')
            blue_ilowH=78
            #blue_ihighH = cv2.getTrackbarPos('highH', 'blue')
            blue_ihighH=138
            #blue_ilowS = cv2.getTrackbarPos('lowS', 'blue')
            blue_ilowS=158
            #blue_ihighS = cv2.getTrackbarPos('highS', 'blue')
            blue_ihighH=255
            #blue_ilowV = cv2.getTrackbarPos('lowV', 'blue')
            blue_ilowV=124
            #blue_ihighV = cv2.getTrackbarPos('highV', 'image')
            blue_ihighV=255
            # get current positions of the trackbars
            #green_ilowH = cv2.getTrackbarPos('lowH', 'green')
            green_ilowH=60
            #green_ihighH = cv2.getTrackbarPos('highH', 'green')
            green_ihighH=75
            #green_ilowS = cv2.getTrackbarPos('lowS', 'green')
            green_ilowS=100
            #green_ihighS = cv2.getTrackbarPos('highS', 'green')
            green_ihighS=255
            #green_ilowV = cv2.getTrackbarPos('lowV', 'green')
            green_ilowV=50
            #green_ihighV = cv2.getTrackbarPos('highV', 'green')
            green_ihighV=255

            #write default vaue range of red,green and blue
            # get current positions of the trackbars
            upper_red_hsv=np.array([red_ihighH, red_ihighS, red_ihighV])
            lower_red_hsv= np.array([red_ilowH, red_ilowS, red_ilowV])
            upper_blue_hsv= np.array([blue_ihighH, blue_ihighS, blue_ihighV])
            lower_blue_hsv=np.array([blue_ilowH, blue_ilowS, blue_ilowV])
            upper_green_hsv=np.array([green_ihighH, green_ihighS, green_ihighV])
            lower_green_hsv=np.array([green_ilowH, green_ilowS, green_ilowV])
            
            #open cv processing
            hsv=cv2.cvtColor(frame,cv2.BGR2HSV)
            gray=cv2.cvtColor(frame,cv2.BGR2GRAY)
            image=cv2.threshold(frame,100,255,cv2.THRESH_BINARY)

            #morphological transformation
            mask_red=cv2.inRange(hsv,lower_red_hsv,upper_red_hsv)
            kernel=np.ones((10,10),np.uint8)
            mask_red=cv2.erode(mask_red,kernel)
            
            mask_blue=cv2.inRange(hsv,lower_blue_hsv,upper_blue_hsv)
            kernel=np.ones((10,10),np.uint8)
            mask_blue=cv2.erode(mask_blue,kernel)
            
            
            mask_green=cv2.inRange(hsv,lower_green_hsv,upper_green_hsv)
            kernel=np.ones((10,10),np.uint8)
            mask_green=cv2.erode(mask_green,kernel)
            
            

            #adaptive threshold can be used to make mask more clear
            
            result_red=cv2.bitwise_and(frame,frame,mask=mask_red)
            result_blue=cv2.bitwise_and(frame,frame,mask=mask_blue)
            result_green=cv2.bitwise_and(frame,frame,mask=mask_green)

                
            
            _,contours_red, _ = cv2.findContours(result_red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            _,contours_blue, _ = cv2.findContours(result_blue, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            _,contours_green, _ = cv2.findContours(result_green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            if cv2.countNonZero(image) == 0:
                ser.write(b'R')
                print('R\n')

            else:
                area_red=[]
                area_blue=[]
                area_green=[]
                #when count is less than 3
                if (var<3):
                
                    for cnt in contours_red:
                        area_red.push(cv2.contourArea(cnt))
                        approx_red=cv2.approxPolyDP(cnt,0.02*cv2.arcLength(cnt,True),True)
                        cv2.drawContours(frame,[cnt],0,(0,0,0),5)
                    maxcontour_red=area_red[0]
                    maxcontour_index=0
                    for x in range(0,contours_red.size()):
                        if (int(maxcontour_red)<int(area_red[x])):
                            maxcontour_index=x
                #box found
                    if(area_red[x]>=0.9*rows*cols):
                        ser.write(b'X')
                        print('X\n')
                        time.sleep(1)
                        var=var+1
                #send box found
                    # compute the center of the contour
                    M = cv2.moments(contours_red[i])
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    if(cX>rows/2+10):
                    #right
                        ser.write(b'R')
                        print('R\n')
                        time.sleep(1)
                    elif(cX<rows/2-10):
                    #left
                        ser.write(b'L')
                        print('L\n')
                        time.sleep(1)
                    elif(cX>=rows/2-10) and (cX<=rows/2+10):
                    #forward
                        ser.write(b'F')
                        print('F\n')
                        time.sleep(1)
                    
                    
                    for cnt in contours_blue:
                        area_blue = cv2.contourArea(cnt)
                        approx_blue=cv2.approxPolyDP(cnt,0.02*cv2.arcLength(cnt,True),True)
                        cv2.drawContours(frame,[cnt],0,(0,0,0),5)
                    maxcontour_blue=area_blue[0]
                    maxcontour_index=0
                    for x in range(0,contours_blue.size()):
                        if (int(maxcontour_blue)<int(area_blue[x])):
                            maxcontour_index=x
                    if(area_blue[x]>0.8*rows*cols):
                    # compute the center of the contour
                        M_blue = cv2.moments(contours_blue[i])
                        cX_blue = int(M_blue["m10"] / M_blue["m00"])
                        cY_blue = int(M_blue["m01"] / M_blue["m00"])
                        
                        if(cX_blue>rows/2+10):
                        #left-right-forward-left-right
                            '''ser.write(b'L')
                            time.sleep(1)
                            ser.write(b'R')
                            time.sleep(1)
                            ser.write(b'F')
                            time.sleep(1)
                            ser.write(b'L')
                            time.sleep(1)
                            ser.write(b'R')
                            time.sleep(1)'''
                            ser.write(b'V')
                            print('V\n')
                            time.sleep(3)
                        elif(cX_blue<rows/2-10):
                        #right-left-forward-right-left
                            '''ser.write(b'R')
                            time.sleep(1)
                            ser.write(b'L')
                            time.sleep(1)
                            ser.write(b'F')
                            time.sleep(1)
                            ser.write(b'R')
                            time.sleep(1)
                            ser.write(b'L')
                            time.sleep(1)'''
                            ser.write(b'W')
                            print('W\n')
                            time.sleep(3)
                        elif(cX_blue<=rows/2+10)and(cX_vlue>=rows/2-10):
                        #forward
                            ser.write(b'F')
                            print('F\n')
                            time.sleep(1)


                #serial reads 3 then start green mode
                    if(var==3):
                        #i.e.allblack
                        if cv2.countNonZero(image) == 0:
                             ser.write(b'R')
                             print('R\n')
                             
                      else:
                            for cnt in contours_green:
                            area_green = cv2.contourArea(cnt)
                            approx_green=cv2.approxPolyDP(cnt,0.02*cv2.arcLength(cnt,True),True)
                            cv2.drawContours(frame,[cnt],0,(0,0,0),5)
                            maxcontour_green=area_green[0]
                            maxcontour_index=0
                            for x in range(0,contours_green.size()):
                                if (int(maxcontour_green)<int(area_green[x])):
                                    maxcontour_index=x
                    #final destination reached
                            if(area_green[x]>=0.9*rows*cols):
                                serial.write('Z')
                                print('Z\n')
                                break
                    #send final destination variable
                        # compute the center of the contour
                            M_green = cv2.moments(contours_green[i])
                            cX_green = int(M_green["m10"] / M_green["m00"])
                            cY_green = int(M_green["m01"] / M_green["m00"])
                            if(cX_green>rows/2):
                                #right
                                ser.write(b'R')
                                print('R\n')
                                time.sleep(0.1)
                            elif(cX_green<rows/2):
                                #left
                                ser.write(b'L')
                                print('L\n')
                                time.sleep(0.1)
                            elif(cX_green==rows/2):
                                #forward
                                ser.write(b'F')
                                print('F\n')
                                time.sleep(0.1)
                            
                        

                            for cnt in contours_blue:
                                area_blue = cv2.contourArea(cnt)
                                approx_blue=cv2.approxPolyDP(cnt,0.02*cv2.arcLength(cnt,True),True)
                                cv2.drawContours(frame,[cnt],0,(0,0,0),5)
                            maxcontour_blue=area_blue[0]
                            maxcontour_index=0
                            for x in range(0,contours_blue.size()):
                                if (int(maxcontour_blue)<int(area_blue[x])):
                                    maxcontour_index=x
                            if(area_blue[x]>0.8*rows*cols):
                            # compute the center of the contour
                                M_blue = cv2.moments(contours_blue[i])
                                cX_blue = int(M_blue["m10"] / M_blue["m00"])
                                cY_blue = int(M_blue["m01"] / M_blue["m00"])
                                
                                if(cX_blue>rows/2+10):
                                #left-right-forward-left-right
                                    '''ser.write(b'L')
                                    time.sleep(1)
                                    ser.write(b'R')
                                    time.sleep(1)
                                    ser.write(b'F')
                                    time.sleep(1)
                                    ser.write(b'L')
                                    time.sleep(1)
                                    ser.write(b'R')
                                    time.sleep(1)'''
                                    ser.write(b'V')
                                    print('V\n')
                                    time.sleep(3)
                                elif(cX_blue<rows/2-10):
                                #right-left-forward-right-left
                                    '''ser.write(b'R')
                                    time.sleep(1)
                                    ser.write(b'L')
                                    time.sleep(1)
                                    ser.write(b'F')
                                    time.sleep(1)
                                    ser.write(b'R')
                                    time.sleep(1)
                                    ser.write(b'L')
                                    time.sleep(1)'''
                                    ser.write(b'W')
                                    print('W\n')
                                    time.sleep(3)
                                elif(cX_blue<=rows/2+10)and(cX_vlue>=rows/2-10):
                                #forward
                                    ser.write(b'F')
                                    time.sleep(1)
                        





        #end
cv2.waitKey(1) & 0xFF == ord('q')
ser.close()
cap.release()
cv2.destroyAllWindows()