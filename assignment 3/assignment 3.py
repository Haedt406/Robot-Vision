import pyrealsense2 as rs
import numpy as np
import cv2
pipeline = rs.pipeline()
config = rs.config()

pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)
device = pipeline_profile.get_device()
device_product_line = str(device.get_info(rs.camera_info.product_line))

tracker = cv2.TrackerKCF_create()

found_rgb = False
for s in device.sensors:
    if s.get_info(rs.camera_info.name) == 'RGB Camera':
        found_rgb = True
        break
if not found_rgb:
    print("The demo requires Depth camera with Color sensor")
    exit(0)

config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

if device_product_line == 'L500':
    config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 30)
    print("true")
else:
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
    print("false")

# Start streaming
profile = pipeline.start(config)
frames = pipeline.wait_for_frames()
depth_frame = frames.get_depth_frame()
color_frame = frames.get_color_frame()
depth_sensor = profile.get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()

print("Depth Scale is: " , depth_scale)

depth_image = np.asanyarray(depth_frame.get_data())
color_image = np.asanyarray(color_frame.get_data())
bbox = cv2.selectROI(color_image, False)
ok = tracker.init(color_image,bbox)
ok, bbox = tracker.update(color_image)  

clipping_distance_in_meters = 1 #1 meter
clipping_distance = clipping_distance_in_meters / depth_scale
align_to = rs.stream.color
align = rs.align(align_to)

try:
    while True:
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()


        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

         
        zDepth = depth_frame.get_distance(int(bbox[0]), int(bbox[1]))
        ok, bbox = tracker.update(color_image) 


        grey_color = 153
        depth_image_3d = np.dstack((depth_image,depth_image,depth_image)) #depth image is 1 channel, color is 3 channels
        bg_removed = np.where((depth_image_3d > clipping_distance) | (depth_image_3d <= 0), grey_color, color_image)
        
        ok, bbox = tracker.update(color_image)
        #check if values are within depth thresholdwhere bbox is updated within the while loop, get finDepth as smoothing out depth with recent depth value as follow: 
        depth1 = depth_frame.get_distance(1, 1)
        depth2 = depth_frame.get_distance(639,479)
        depth3 = depth_frame.get_distance(int(depth1),int(depth2))

        # print("int(bbox[0]) + int(bbox[2]))" + str(int(bbox[0])) + str(int(bbox[2])))
        try:
            zDepth = depth_frame.get_distance(int(bbox[0]) + int(bbox[2]), int(depth3))
        except:
            zDepth = depth_frame.get_distance(int(bbox[0]) - int(bbox[2]), int(depth3))
        # depthThresh = depth2=depth1
        depthList = []

        if ok:
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2])) ,int(bbox[1] + bbox[3])
            cv2.rectangle(color_image, p1,p2,(0,0,255),2,2)

            # if depth_to_object < depthThresh:
            #     depth_to_object = depthThresh
            # elif depth_to_object > depthThresh + 1.0: 
            #     depth_to_object = depthThresh + 1.0
            # depthList.append(depth_to_object)
            # if len(depthList) > 15:
            #     depthList.pop(0)
            # finDepth = sum(depthList) / len(depthList)
        else:
        # Tracking failure
            cv2.putText(color_image, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,
                    (0, 0, 255), 2)

        if ok:
            cv2.putText(color_image, "Distance: "+ str(zDepth), (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,
                        (0, 0, 255), 2)

        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_OCEAN)
       
        images = np.hstack((color_image, depth_colormap))
        # Show images
        images_shape = images.shape
        black_screen = np.zeros((images_shape[0], images_shape[1], 3), np.uint8)
        cv2.line(black_screen,      (int(bbox[0]), int(bbox[1]))   ,    ((int(bbox[2]), int(bbox[3])))   ,  (255,2,0))
        cv2.circle(black_screen, (320,240), 22, (0,0,255), 2)
        # black_screen = cv2.applyColorMap(cv2.convertScaleAbs(bg_removed, alpha=0.03), cv2.COLORMAP_JET)
       
        
        # scaling = images.size
        # center = images.size/2
        # xStart = bbox[0] - int(finDepth * scaling) + 300
        # xEnd = bbox[0] + bbox[2] - int(finDepth * scaling)
        # y = int(center[0] - finDepth * scaling)
        # cv2.line(black_screen, (xStart, y), (xEnd, y), (255, 0, 0))
        depth_colormap_dim = depth_colormap.shape
        color_colormap_dim = color_image.shape
        if depth_colormap_dim != color_colormap_dim:
            resized_color_image = cv2.resize(color_image, dsize=(depth_colormap_dim[1], depth_colormap_dim[0]), interpolation=cv2.INTER_AREA)
            images = np.hstack((resized_color_image, depth_colormap))
        else:
            images = np.hstack((color_image, depth_colormap))
        images = np.vstack((images, black_screen))
        # cv2.imshow('RealSense', stacked)
        cv2.namedWindow('RealSense', cv2.WINDOW_NORMAL)
        cv2.imshow('RealSense', images)

        cv2.waitKey(1)

finally:
    pipeline.stop()
