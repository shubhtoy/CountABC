from flask import Flask, render_template, make_response, redirect, send_from_directory
from flask import request
import os
app = Flask(__name__)

# Set a strong secret key for session management and security.
app.secret_key = 'Shubh@KIIT'


@app.route('/')
def index():
    return render_template("index.html")


# Define URLs to include in the sitemap
sitemap_urls = [
    'https://countabc.xyz/',  # Include the homepage in the sitemap
    # Add more URLs as needed
]


@app.route('/sitemap.xml/')
def sitemap():
    # Define the path to your sitemap file
    # sitemap_path = 'static/webmaster/sitemap.xml'

    # Check if the sitemap file exists
    # if os.path.exists(sitemap_path):
    #     # Read the sitemap content from the file
    #     with open(sitemap_path, 'r') as file:
    #         sitemap_xml = file.read()

    #     # Create a response with the sitemap content
    #     response = make_response(sitemap_xml)
    #     response.headers['Content-Type'] = 'application/xml'
    #     return response
    # else:
    #     # Handle the case where the sitemap file doesn't exist
    #     return "Sitemap not found", 404
    return send_from_directory(app.static_folder, request.path[1:])

# Catch-all route to redirect any other request to the home page.


@app.route("/<path:invalid_path>")
def redirect_to_home(invalid_path):
    return redirect('/')


if __name__ == "__main__":
    # Use Gunicorn as the production-ready server.
    # You can adjust the number of workers (-w) as needed for your application.
    app.run(debug=True)
    # https
    # waitress.serve(app, host='0.0.0.0', port=443, url_scheme='https')
