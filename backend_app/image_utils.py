# backend_app/image_utils.py
import cv2
import roop.globals
import roop.metadata
import roop.utilities as util
from roop.core import set_execution_provider,InitPlugins,get_processing_plugins
from roop.face_util import extract_face_images
from roop.capturer import get_image_frame
import roop.globals
from settings import Settings

def process_image(src_image, dst_image, input_face_index, output_face_index):
    try:
        if src_image is None:
            print("Source image is missing.")
            return None

        if dst_image is None:
            print("Destination image is missing.")
            return None

        if (roop.globals.CFG == None):
            roop.globals.CFG = Settings('config.yaml')
            set_execution_provider(roop.globals.CFG.provider)
            InitPlugins()
            # print(f'Available providers {roop.globals.execution_providers}, using {roop.globals.execution_providers[0]} - Device:{util.get_device()}')

        default_select_src_index = input_face_index
        default_select_dst_index = output_face_index #暂时无效
        src_face = []
        dst_face = []
        src_all_faces = extract_face_images(src_image,  (False, 0))
        dst_all_faces = extract_face_images(dst_image,  (False, 0))

        num_faces = len(src_all_faces) - 1
        print("num_faces:", num_faces)
        if (default_select_src_index > num_faces):
            default_select_src_index = 0

        num_faces = len(dst_all_faces) - 1
        print("num_faces:", num_faces)
        if (default_select_dst_index > num_faces):
            default_select_dst_index = 0

        src_face.append(src_all_faces[default_select_src_index][0])
        dst_face.append(dst_all_faces[default_select_dst_index][0])
        face_info = dst_face[0]  # 获取第一个人脸的信息，包括坐标信息
        startX, startY, endX, endY = face_info['bbox'].astype("int")  # 解包坐标信息


        # 打印坐标信息
        print(f"Destination Face Coordinates:")
        print(f"startX: {startX}, startY: {startY}, endX: {endX}, endY: {endY}")

        return swap_faces(dst_image, src_face, dst_face)
    except Exception as e:
        print(f"Error in process_image: {e}")
        return None

# 功能1：获取输入人脸
def get_all_face_from_image(image):
    faces_data = None
    faces_data = extract_face_images(image,  (False, 0))
    if faces_data is None:
        print("No faces were detected in the source image.")
        return None
    else:
        return faces_data

# 功能2：交换人脸
def swap_faces(target_file, src_face, dst_face):
    processors = get_processing_plugins(False)
    current_frame = get_image_frame(target_file)
    if current_frame is None:
        print("swap_faces input image is missing.")
        return None

    try:
        temp_frame, _ = roop.globals.IMAGE_CHAIN_PROCESSOR.run_chain(current_frame,
                                                        {"swap_mode": roop.globals.face_swap_mode,
                                                            "original_frame": current_frame,
                                                            "blend_ratio": roop.globals.blend_ratio,
                                                            "selected_index": 0,
                                                            "face_distance_threshold": roop.globals.distance_threshold,
                                                            "input_face_datas": src_face,
                                                            "target_face_datas": dst_face,
                                                            "clip_prompt": ""},
                                                            processors)
    except Exception as e:
        print("IMAGE_CHAIN_PROCESSOR:An error occurred while processing temp_frame:", e)
        return None
    return temp_frame