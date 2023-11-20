import cv2
from pyzbar.pyzbar import decode

# Initialize the video capture device
cap = cv2.VideoCapture(0)  # 0 for default camera

while True:
    # Capture the current frame
    ret, frame = cap.read()

    # Check if the frame was successfully captured
    if ret:
        # Convert the frame to HSV color space
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Extract the V channel (brightness)
        brightness_channel = hsv_frame[:, :, 2]

        # Normalize the brightness channel
        normalized_brightness = cv2.normalize(brightness_channel, None, 0, 255, cv2.NORM_MINMAX)

        # Convert the normalized brightness back to BGR color space
        normalized_frame = cv2.cvtColor(normalized_brightness[:, :, None], cv2.COLOR_GRAY2BGR)

        # Decode the barcodes in the normalized frame
        decoded_objects = decode(normalized_frame)

        # Draw bounding boxes and data around detected barcodes
        for obj in decoded_objects:
            x, y, w, h = obj.rect
            
            barcode_data = str(obj.data)
            
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, barcode_data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # Display the processed frame
        cv2.imshow('Barcode Reader', frame)

        # Check for 'q' key to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release the video capture device and close all windows
cap.release()
cv2.destroyAllWindows()

