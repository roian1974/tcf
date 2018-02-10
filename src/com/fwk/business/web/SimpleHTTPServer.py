import http.server

httpd = http.server.HTTPServer(('0.0.0.0', 8080), http.server.SimpleHTTPRequestHandler)

httpd.serve_forever()