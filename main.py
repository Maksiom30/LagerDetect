import http.server
import socketserver
import mkPic
import LagerDetect.detect as detect
import cv2 as cv

# Define a custom request handler by subclassing http.server.SimpleHTTPRequestHandler
class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Handle GET request
        self.send_response(200)
        

        print(self.path)
        print(self.path.replace("/grey/", ""))
        raw = mkPic.mkPic()
        frame, count = detect.detect_bottles(raw)
        
        if self.path == "/img":
            self.send_header('Content-type', 'image/jpeg')
            self.end_headers()
            cv.imwrite("img.jpg", frame)

            with open("img.jpg", "rb") as file:
                img = file.read()
                file.close()

            self.wfile.write(img)
        if self.path == "/":
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html =f"""
<!DOCTYPE html>
<html lang="en">
<title>Img</title>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LagerDetect</title>
</head>
<body>
    <h1>Es gibt ungefär {count} flaschen.</h1>
</body>
</html>
"""

            self.wfile.write(str.encode(html))
        

PORT = 8000

# Create the HTTP server and bind it to the specified port with the custom handler
socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
    print(f"Serving HTTP on port {PORT}")
    
    # Serve the HTTP server until interrupted
    httpd.serve_forever()
