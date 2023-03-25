# import pyrealsense2 as rs
# import numpy as np
# import cv2
# # from mask_rcnn import *
# # Configure depth and color streams
# pipeline = rs.pipeline()
# config = rs.config()

# # Get device product line for setting a supporting resolution
# pipeline_wrapper = rs.pipeline_wrapper(pipeline)
# pipeline_profile = config.resolve(pipeline_wrapper)
# device = pipeline_profile.get_device()
# device_product_line = str(device.get_info(rs.camera_info.product_line))

# tracker = cv2.TrackerKCF_create()

# found_rgb = False
# for s in device.sensors:
#     if s.get_info(rs.camera_info.name) == 'RGB Camera':
#         found_rgb = True
#         break
# if not found_rgb:
#     print("The demo requires Depth camera with Color sensor")
#     exit(0)

# config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

# if device_product_line == 'L500':
#     config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 30)
# else:
#     config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# # Start streaming
# profile = pipeline.start(config)
# frames = pipeline.wait_for_frames()
# depth_frame = frames.get_depth_frame()
# color_frame = frames.get_color_frame()
# depth_sensor = profile.get_device().first_depth_sensor()
# depth_scale = depth_sensor.get_depth_scale()

# print("Depth Scale is: " , depth_scale)

# depth_image = np.asanyarray(depth_frame.get_data())
# color_image = np.asanyarray(color_frame.get_data())
# bbox = cv2.selectROI(color_image, False)
# ok = tracker.init(color_image,bbox)
# ok, bbox = tracker.update(color_image)  

# clipping_distance_in_meters = 1 #1 meter
# clipping_distance = clipping_distance_in_meters / depth_scale
# align_to = rs.stream.color
# align = rs.align(align_to)

# try:
#     while True:
#         frames = pipeline.wait_for_frames()
#         depth_frame = frames.get_depth_frame()
#         color_frame = frames.get_color_frame()

#         aligned_frames = align.process(frames)
#         aligned_depth_frame = aligned_frames.get_depth_frame() # aligned_depth_frame is a 640x480 depth image
#         color_frame = aligned_frames.get_color_frame()

#         if not depth_frame or not color_frame:
#             continue
#         # depth_image = np.asanyarray(depth_frame.get_data())
#         color_image = np.asanyarray(color_frame.get_data())

#         grey_color = 153
#         depth_image_3d = np.dstack((depth_image,depth_image,depth_image)) #depth image is 1 channel, color is 3 channels
#         bg_removed = np.where((depth_image_3d > clipping_distance) | (depth_image_3d <= 0), grey_color, color_image)
        
#         ok, bbox = tracker.update(color_image)  
#         zDepth = depth_frame.get_distance(int(bbox[0]), int(bbox[1]))
#         # depthList = [zDepth]
#         # depthThresh = zDepth
#         # if depth_to_object < depthThresh:
#         #     depth_to_object = depthThresh
#         # elif depth_to_object > depthThresh + 1.0: 
#         #     depth_to_object = depthThresh + 1.0
#         # depthList.append(depth_to_object)
#         # if len(depthList) > 15:
#         #     depthList.pop(0)
#         # finDepth = sum(depthList) / len(depthList)


#         if ok:
#             p1 = (int(bbox[0]), int(bbox[1]))
#             p2 = (int(bbox[0] + bbox[2])) ,int(bbox[1] + bbox[3])
#             cv2.rectangle(color_image, p1,p2,(0,0,255),2,2)
#         else:
#         # Tracking failure
#             cv2.putText(color_image, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,
#                     (0, 0, 255), 2)

#         if ok:
#             cv2.putText(color_image, "Distance: "+ str(zDepth), (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,
#                         (0, 0, 255), 2)

#         # depthThresh = color_image.get

#         # if depth_to_object < depthThresh:
#         #     depth_to_object = depthThresh
#         # elif depth_to_object > depthThresh + 1.0: 
#         #     depth_to_object = depthThresh + 1.0
#         # depthList.append(depth_to_object)
#         # if len(depthList) > 15:
#         #     depthList.pop(0)
#         # finDepth = sum(depthList) / len(depthList)
#         # if ok:
#         #     xStart = bbox[0] - int(finDepth * scaling) + 300
#         #     xEnd = bbox[0] + bbox[2] - int(finDepth * scaling)
#         #     y = int(center[0] - finDepth * scaling)
#             # cv2.line(black_screen, (xStart, y), (xEnd, y), (255, 0, 0))
#         # xStart = bbox[0] - int(finDepth * scaling) + 300
#         # xEnd = bbox[0] + bbox[2] - int(finDepth * scaling)
#         # y = int(center[0] - finDepth * scaling)
#         # cv2.line(blank_image, (xStart, y), (xEnd, y), (255, 0, 0))
#         # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
#         depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_OCEAN)
#         # depth_colormap_dim = depth_colormap.shape
#         # color_colormap_dim = color_image.shape
#         # If depth and color resolutions are different, resize color image to match depth image for display
#         # if depth_colormap_dim != color_colormap_dim:
#         #     resized_color_image = cv2.resize(color_image, dsize=(depth_colormap_dim[1], depth_colormap_dim[0]), interpolation=cv2.INTER_AREA)
#         #     images = np.hstack((resized_color_image, depth_colormap))
#         # else:
#         # images = np.hstack((color_image, bg_removed))
#         images = np.hstack((color_image, depth_colormap))
#         # Show images
#         images_shape = images.shape
#         black_screen = np.zeros((images_shape[0], images_shape[1], 3), np.uint8)
#         # black_screen = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
       

#         images = np.vstack((images, black_screen))

#         cv2.namedWindow('RealSense', cv2.WINDOW_NORMAL)
#         cv2.imshow('RealSense', images)

#         cv2.waitKey(1)

# finally:
#     pipeline.stop()








import pyrealsense2 as rs
import numpy as np
import cv2

# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()

# Get device product line for setting a supporting resolution
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
else:
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
profile = pipeline.start(config)

frames = pipeline.wait_for_frames()
depth_frame = frames.get_depth_frame()

color_frame = frames.get_color_frame()

depth_sensor = profile.get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()

# Convert images to numpy arrays
depth_image = np.asanyarray(depth_frame.get_data())
color_image = np.asanyarray(color_frame.get_data())


bbox = cv2.selectROI(color_image, False)
ok = tracker.init(color_image,bbox)
ok, bbox = tracker.update(color_image)  
# if ok:
#     p1 = (int(bbox[0]), int(bbox[1]))
#     p2 = (int(bbox[0] + bbox[2])) ,int(bbox[1] + bbox[3])
#     cv2.rectangle(frames, p1,p2,(0,0,255),2,2)

try:
    while True:

        # zDepth = depth_frame.get_distance(bbox)
        # ir_frame = frames.get_infrared_frame()
        # intrin = ir_frame.profile.as_video_stream_profile().intrinsics

        # # get pixels' depth
        # depth1 = depth_frame.get_distance(x1, y1)
        # depth2 = depth_frame.get_distance(x2, y2)

        # project pixels onto 3D plane based on their depth
        # project data onto intrinsics of infrared frame
        # p1 = rs.rs2_deproject_pixel_to_point(intrin, [x1, y1], depth1)
        # p2 = rs.rs2_deproject_pixel_to_point(intrin, [x2, y2], depth2)

        # compute distance
        # dist = np.sqrt(np.power((p1[0] - p2[0]), 2) + np.power((p1[1] - p2[1]), 2) + np.power((p1[2] - p2[2]), 2))

        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()

        if not depth_frame or not color_frame:
            continue
        # Convert images to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        
        ok, bbox = tracker.update(color_image)  
        zDepth = depth_frame.get_distance(int(bbox[0]), int(bbox[1]))

        if ok:
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2])) ,int(bbox[1] + bbox[3])
            cv2.rectangle(color_image, p1,p2,(0,0,255),2,2)

        if ok:
            cv2.putText(color_image, "Distance: "+ str(zDepth), (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,
                        (0, 0, 255), 2)

        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
        depth_colormap_dim = depth_colormap.shape
        color_colormap_dim = color_image.shape
        # If depth and color resolutions are different, resize color image to match depth image for display
        if depth_colormap_dim != color_colormap_dim:
            resized_color_image = cv2.resize(color_image, dsize=(depth_colormap_dim[1], depth_colormap_dim[0]), interpolation=cv2.INTER_AREA)
            images = np.hstack((resized_color_image, depth_colormap))
        else:
            images = np.hstack((color_image, depth_colormap))
        # Show images
        images_shape = images.shape
        black_screen = np.zeros((images_shape[0], images_shape[1], 3), np.uint8)

        images = np.vstack((images, black_screen))

        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', images)

        cv2.waitKey(1)

finally:
    pipeline.stop()





# import pyrealsense2 as rs
# import numpy as np
# import cv2

# # Configure depth and color streams
# pipeline = rs.pipeline()
# config = rs.config()

# # Get device product line for setting a supporting resolution
# pipeline_wrapper = rs.pipeline_wrapper(pipeline)
# pipeline_profile = config.resolve(pipeline_wrapper)
# device = pipeline_profile.get_device()
# device_product_line = str(device.get_info(rs.camera_info.product_line))

# tracker = cv2.TrackerKCF_create()

# # cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)

# found_rgb = False
# for s in device.sensors:
#     if s.get_info(rs.camera_info.name) == 'RGB Camera':
#         found_rgb = True
#         break
# if not found_rgb:
#     print("The demo requires Depth camera with Color sensor")
#     exit(0)

# config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

# if device_product_line == 'L500':
#     config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 30)
# else:
#     config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# # Start streaming
# profile = pipeline.start(config)

# frames = pipeline.wait_for_frames()
# depth_frame = frames.get_depth_frame()
# color_frame = frames.get_color_frame()

# depth_sensor = profile.get_device().first_depth_sensor()
# depth_scale = depth_sensor.get_depth_scale()

# # Convert images to numpy arrays
# depth_image = np.asanyarray(depth_frame.get_data())
# color_image = np.asanyarray(color_frame.get_data())


# bbox = cv2.selectROI(color_image, False)
# ok = tracker.init(color_image,bbox)
# ok, bbox = tracker.update(color_image)  
# # if ok:
# #     p1 = (int(bbox[0]), int(bbox[1]))
# #     p2 = (int(bbox[0] + bbox[2])) ,int(bbox[1] + bbox[3])
# #     cv2.rectangle(frames, p1,p2,(0,0,255),2,2)

# try:
#     while True:

#         # zDepth = depth_frame.get_distance(bbox)

#         # ir_frame = frames.get_infrared_frame()
#         # intrin = ir_frame.profile.as_video_stream_profile().intrinsics

#         # # get pixels' depth
#         # depth1 = depth_frame.get_distance(x1, y1)
#         # depth2 = depth_frame.get_distance(x2, y2)

#         # project pixels onto 3D plane based on their depth
#         # project data onto intrinsics of infrared frame
#         # p1 = rs.rs2_deproject_pixel_to_point(intrin, [x1, y1], depth1)
#         # p2 = rs.rs2_deproject_pixel_to_point(intrin, [x2, y2], depth2)

#         # compute distance
#         # dist = np.sqrt(np.power((p1[0] - p2[0]), 2) + np.power((p1[1] - p2[1]), 2) + np.power((p1[2] - p2[2]), 2))

#         # Wait for a coherent pair of frames: depth and color
#         frames = pipeline.wait_for_frames()
#         depth_frame = frames.get_depth_frame()
#         color_frame = frames.get_color_frame()

#         if not depth_frame or not color_frame:
#             continue
#         # Convert images to numpy arrays
#         depth_image = np.asanyarray(depth_frame.get_data())
#         color_image = np.asanyarray(color_frame.get_data())
        
#         ok, bbox = tracker.update(color_image)  

#         if ok:
#             p1 = (int(bbox[0]), int(bbox[1]))
#             p2 = (int(bbox[0] + bbox[2])) ,int(bbox[1] + bbox[3])
#             cv2.rectangle(color_image, p1,p2,(0,0,255),2,2)

#         # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
#         depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
#         depth_colormap_dim = depth_colormap.shape
#         color_colormap_dim = color_image.shape
#         # If depth and color resolutions are different, resize color image to match depth image for display
#         if depth_colormap_dim != color_colormap_dim:
#             resized_color_image = cv2.resize(color_image, dsize=(depth_colormap_dim[1], depth_colormap_dim[0]), interpolation=cv2.INTER_AREA)
#             images = np.hstack((resized_color_image, depth_colormap))
#         else:
#             images = np.hstack((color_image, depth_colormap))
#         # Show images
#         images_shape = images.shape
#         black_screen = np.zeros((images_shape[0], images_shape[1], 3), np.uint8)

#         images = np.vstack((images, black_screen))

#         cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
#         cv2.imshow('RealSense', images)

#         cv2.waitKey(1)

# finally:
#     pipeline.stop()

