TODO:
look into fabric.js
look into canvas api

**fast api server**
testing: `fastapi dev main.py`
testing: `fastapi run main.py`

**frontent**
`npm run dev`


    Find all connected components by using find FindContour method

    Store contour for every Region (Connected componnet CC)

    calculate the Bounding Rect for every region (CC)

    Loop in all region

    For every region , find the nearest regions depending on the Bounding rect

    now you have the suspected regions which can be connected to region, compare the two contours and find the mimimum distance between the two contours , if the minimum distance is smaller than threshould (say 10 pixel) then now you can draw line from Point1 in first contour and point2 in second contour , Point1 and Point2 are the points which satisfy the minmum distance calculated before.

    repeat the proces for all regions

https://answers.opencv.org/question/70629/detect-spaces-and-fill-with-rectangle/
