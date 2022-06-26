import cv2
import math
import numpy as np
import scipy.ndimage
import logging

logging.basicConfig(level='INFO')
log = logging.getLogger("CrackDetection")


class CrackDetection:
    __instance = None

    @staticmethod
    def get_instance():
        if CrackDetection.__instance is None:
            return CrackDetection()
        log.info("Fetching CrackDetection Instance")
        return CrackDetection.__instance

    def __init__(self):
        if CrackDetection.__instance is not None:
            log.info("Crack Detection Instance is not None")
        else:
            self.test = ""

    def orientated_non_max_suppression(self, mag, ang):
        ang_quant = np.round(ang / (np.pi / 4)) % 4
        winE = np.array([[0, 0, 0], [1, 1, 1], [0, 0, 0]])
        winSE = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        winS = np.array([[0, 1, 0], [0, 1, 0], [0, 1, 0]])
        winSW = np.array([[0, 0, 1], [0, 1, 0], [1, 0, 0]])

        magE = self.non_max_suppression(mag, winE)
        magSE = self.non_max_suppression(mag, winSE)
        magS = self.non_max_suppression(mag, winS)
        magSW = self.non_max_suppression(mag, winSW)

        mag[ang_quant == 0] = magE[ang_quant == 0]
        mag[ang_quant == 1] = magSE[ang_quant == 1]
        mag[ang_quant == 2] = magS[ang_quant == 2]
        mag[ang_quant == 3] = magSW[ang_quant == 3]
        return mag

    def non_max_suppression(self, data, win):
        data_max = scipy.ndimage.filters.maximum_filter(data, footprint=win, mode='constant')
        data_max[data != data_max] = 0
        return data_max

    # start calulcation
    # cv2.namedWindow("Grab")
    def detect_function(self, path):
        # cam = cv2.VideoCapture(1)
        # while True:
        #     ret, frame = cam.read()
        #     if not ret:
        #         print("failed to grab frame")
        #         break
        #     cv2.imshow("Grab Frame", frame)
        #
        #     k = cv2.waitKey(1)
        #     if k % 256 == 27:
        #         # ESC pressed
        #         print("Escape hit, closing...")
        #         break
        #     elif k % 256 == 32:
        #         # SPACE pressed
        #         img_name = "crack.jpeg"
        #         cv2.imwrite(img_name, frame)
        # cam.release()
        # cv2.destroyAllWindows()
        gray_image = cv2.imread(r'/home/gaurav/Desktop/gphoto/images/' + path, 0)
        with_nmsup = True  # apply non-maximal suppression
        fudgefactor = 1.3  # with this threshold you can play a little bit
        sigma = 21  # for Gaussian Kernel
        kernel = 2 * math.ceil(2 * sigma) + 1  # Kernel size

        gray_image = gray_image / 255.0
        blur = cv2.GaussianBlur(gray_image, (kernel, kernel), sigma)
        gray_image = cv2.subtract(gray_image, blur)

        # compute sobel response
        sobelx = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=3)
        mag = np.hypot(sobelx, sobely)
        ang = np.arctan2(sobely, sobelx)

        # threshold
        threshold = 4 * fudgefactor * np.mean(mag)
        mag[mag < threshold] = 0

        # either get edges directly
        if with_nmsup is False:
            mag = cv2.normalize(mag, 0, 255, cv2.NORM_MINMAX)
            kernel = np.ones((5, 5), np.uint8)
            result = cv2.morphologyEx(mag, cv2.MORPH_CLOSE, kernel)
            cv2.imshow('im', result)
            cv2.waitKey()

        # or apply a non-maximal suppression
        else:

            # non-maximal suppression
            mag = self.orientated_non_max_suppression(mag, ang)
            # create mask
            mag[mag > 0] = 255
            mag = mag.astype(np.uint8)

            kernel = np.ones((5, 5), np.uint8)
            result = cv2.morphologyEx(mag, cv2.MORPH_CLOSE, kernel)

            cv2.imshow('im', result)
            cv2.waitKey()


# if __name__ == "__main_":
#     crack_detection = CrackDetection.get_instance()
#     camera = Camera.get_instance()
#     file = camera.run()
#     crack_detection.detect_function(file)