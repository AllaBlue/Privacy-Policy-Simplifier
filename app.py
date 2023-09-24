from flask import Flask, request, jsonify, render_template
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

from credentials import work_related_credentials


app = Flask(__name__)


# Function to scan the form for work credentials using Selenium
def scan_form_for_work_credentials(url):
    print("URL to check:", url)

    driver = webdriver.Chrome()

    try:
        # Navigate to the URL
        driver.get(url)

        # Wait for the page to load (you might need to adjust the time based on your webpage)
        driver.implicitly_wait(10)  # Wait for 10 seconds

        # Find all input elements
        input_elements = driver.find_elements(By.TAG_NAME, "input")

        # Extract names of all input elements
        input_names = [
            element.get_attribute("name")
            for element in input_elements
            if element.get_attribute("name")
        ]

        print("Input names:", input_names)

        # Check if any input for work credentials was found
        has_work_credentials = any(
            name in work_related_credentials for name in input_names
        )
        return has_work_credentials

    finally:
        # Close the browser
        driver.quit()


@app.route("/scan-form", methods=["GET"])
def scan_form():
    url = request.args.get("url")

    if url:
        has_work_credentials = scan_form_for_work_credentials(url)
        if has_work_credentials:
            return render_template("error.html")
        else:
            return render_template("success.html")

    return jsonify({"error": "No URL provided"}), 400


@app.route("/scan-form/<path:url>", methods=["GET"])
def scan_form_url(url):
    has_work_credentials = scan_form_for_work_credentials(url)
    return jsonify({"has_work_credentials": has_work_credentials})


@app.route("/", methods=["GET"])
def render_home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
