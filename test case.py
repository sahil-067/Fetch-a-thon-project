import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class QRCodeScannerApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        self.video_source = 0
        self.cap = cv2.VideoCapture(self.video_source)

        # Create a QR code detector
        self.qr_code_detector = cv2.QRCodeDetector()

        # Create a canvas to display the video feed
        self.canvas = tk.Canvas(window, width=self.cap.get(3), height=self.cap.get(4))
        self.canvas.pack()

        # Create Refresh and Scan Again buttons
        self.refresh_button = ttk.Button(window, text="Refresh", command=self.refresh)
        self.refresh_button.pack(padx=10, pady=5, side=tk.LEFT)

        self.scan_again_button = ttk.Button(window, text="Scan Again", command=self.scan_again)
        self.scan_again_button.pack(padx=10, pady=5, side=tk.RIGHT)

        self.update()
        self.window.mainloop()

    def refresh(self):
        # Release the current video capture object
        self.cap.release()

        # Increment the video source to switch cameras if available
        self.video_source += 1

        # Open a new video capture object
        self.cap = cv2.VideoCapture(self.video_source)

        # Update the canvas size
        self.canvas.config(width=self.cap.get(3), height=self.cap.get(4))

    def scan_again(self):
        # Read a frame from the camera
        ret, frame = self.cap.read()

        # Detect and decode QR codes
        value, pts, qr_code_data = self.qr_code_detector.detectAndDecode(frame)

        # Check if a QR code is detected
        if value:
            # Print the QR code data to the console
            print("QR Code Data:", qr_code_data)

    def update(self):
        # Read a frame from the camera
        ret, frame = self.cap.read()

        if ret:
            # Detect and decode QR codes
            value, pts, qr_code_data = self.qr_code_detector.detectAndDecode(frame)

            # Check if a QR code is detected
            if value:
                # Draw a smoothed rectangle around the QR code
                approx = cv2.approxPolyDP(pts, 0.4 * cv2.arcLength(pts, True), True)
                cv2.polylines(frame, [approx], isClosed=True, color=(0, 255, 0), thickness=2)

                # Display the QR code data
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame, qr_code_data, (int(approx[0][0][0]), int(approx[0][0][1]) - 10),
                            font, 0.5, (0, 255, 0), 2, cv2.LINE_AA)

            # Convert the frame to RGB format and then to ImageTk format
            img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            img_tk = ImageTk.PhotoImage(image=img)

            # Update the canvas with the new image
            self.canvas.img = img_tk
            self.canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)

        # Schedule the update after 10 milliseconds
        self.window.after(10, self.update)

    def __del__(self):
        # Release the video capture object when the app is closed
        if self.cap.isOpened():
            self.cap.release()

# Create the main window
root = tk.Tk()

# Create the QRCodeScannerApp instance
app = QRCodeScannerApp(root, "QR Code Scanner")

# Run the application
root.mainloop()
