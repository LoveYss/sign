# Author:Loveyss
# -*-coding:utf-8 -*-
# @Time     :2019/6/17   9:47
# @Author   :Loveyss
# @Site     :
# @File     :know_face.py
# @Software :PyCharm

import face_recognition


def validation(user_img_path):
    user_img = face_recognition.load_image_file(user_img_path)
    unknown_img = face_recognition.load_image_file('static\\images\\unknown_user_img.jpg')
    """
    获取每个图像文件中每个面部的面部编码
    由于每个图像中可能有多个面，所以返回一个编码列表
    但是由于我知道每个图像只有一个脸，我只关心每个图像中的第一个编码，所以我取索引0
    """
    try:
        user_face_encoding = face_recognition.face_encodings(user_img)[0]
        unknown_face_encoding = face_recognition.face_encodings(unknown_img)[0]
    except Exception as e:
        return False

    known_faces = [
        user_face_encoding
    ]
    """
    结果是True/false的数组，未知面孔known_faces阵列中的任何人相匹配的结果
    """
    results = face_recognition.compare_faces(known_faces, unknown_face_encoding, tolerance=0.3)
    return results[0]


if __name__ == '__main__':
    print(validation('F:\\sign\\static\\images\\user_img.jpg'))
