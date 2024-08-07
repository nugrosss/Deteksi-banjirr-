import cv2 as cv
import numpy as np
import threading
import tkinter as tk
from vision import Vision
from gui import ScaleApp

class VideoProcessor:
    def __init__(self, video_source, scale_app):
        self.cap = Vision(addr=video_source)
        self.scale_app = scale_app

    def process(self):
        while True:
            # Baca frame
            frame = self.cap.read(frame_size=720)
            
            if frame is None:
                print("Video Berhenti")
                break

            # Ubah ukuran frame (jika diperlukan, jika sudah diubah ukurannya di metode read, lewati ini)
            frame_resized = self.cap.resize(frame, width=720)

            # Konversi frame ke HSV
            frame_hsv = self.cap.frame_hsv(frame_resized)
            
            if frame_hsv is None or frame_hsv.size == 0:
                print("Gagal mengonversi frame ke HSV")
                break

            # Dapatkan nilai skala dari GUI
            lower_hue = self.scale_app.hue_low_scale.get()
            lower_sat = self.scale_app.saturation_low_scale.get()
            lower_val = self.scale_app.value_low_scale.get()
            upper_hue = self.scale_app.hue_high_scale.get()
            upper_sat = self.scale_app.saturation_high_scale.get()
            upper_val = self.scale_app.value_high_scale.get()

            # define range  color in HSV
            lower_red1 = np.array([lower_hue, lower_sat, lower_val])
            upper_red1 = np.array([upper_hue, upper_sat, upper_val])

            # Threshold the HSV image to get only specified colors
            mask = cv.inRange(frame_hsv, lower_red1, upper_red1)

            # Bitwise-AND mask and original image
            res = cv.bitwise_and(frame_resized, frame_resized, mask=mask)

            # Temukan kontur dalam frame mask
            contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

            for cnt in contours:
                # Hitung bounding box untuk setiap kontur
                x, y, w, h = cv.boundingRect(cnt)
                area = cv.contourArea(cnt)

                # Definisikan kepadatan piksel minimum dan ambang batas untuk status
                flood_threshold_low = 200
                flood_threshold_high = 500

                if area > flood_threshold_low:
                    # Gambar bounding box pada frame asli
                    cv.rectangle(frame_resized, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    # Tambahkan label area
                    cv.putText(frame_resized, f'Area: {area}', (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                    # Perbaiki logika cetak status
                    if area < flood_threshold_low:
                        print(f"{area}==""Banjirrrr")
                    elif flood_threshold_low <= area < flood_threshold_high:
                        print(f"{area}==""Siaga")
                    else:
                        print(f"{area}==""Aman")
                

            # Tampilkan frame yang sudah diubah ukurannya dan diubah ke HSV
            cv.imshow('frame', frame_resized)
            cv.imshow('mask', mask)
            cv.imshow('res', res)
            
            if cv.waitKey(1) == ord('q'):
                break

        self.cap.cap.release()
        cv.destroyAllWindows()



def start_video_processing(scale_app):
    video_processor = VideoProcessor(video_source="// your vidio", scale_app=scale_app)
    video_processor.process()

if __name__ == "__main__":
    # Inisialisasi GUI
    root = tk.Tk()
    scale_app = ScaleApp(root)

    # Jalankan pemrosesan video dalam thread terpisah
    video_thread = threading.Thread(target=start_video_processing, args=(scale_app,))
    video_thread.start()

    # Jalankan loop utama GUI
    root.mainloop()

    # Tunggu thread pemrosesan video selesai
    video_thread.join()
