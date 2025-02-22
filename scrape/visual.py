from selenium import webdriver
from selenium.webdriver.common.by import By  # Ensure this import is included
from selenium.webdriver.chrome.options import Options
from PIL import Image
import io
import base64
from IPython.display import display

# Set up Chrome options for headless mode (no UI)
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")


driver = webdriver.Chrome(options=chrome_options)

driver.get('https://stockanalysis.com/stocks/aapl/')

# Wait for the page to load (adjust the waiting time if needed)
driver.implicitly_wait(10)

# Use JavaScript to capture the base64 image data from the canvas
canvas_element = driver.find_element(By.TAG_NAME, 'canvas')

# Execute JavaScript to extract the canvas image data as base64
canvas_data = driver.execute_script("""
    var canvas = arguments[0];
    return canvas.toDataURL('image/png');  // Get image data in base64 PNG format
""", canvas_element)

# The result is a data URL, so we need to extract the base64 part
image_data = canvas_data.split(',')[1]

# Decode the base64 string and save it as an image
image_bytes = base64.b64decode(image_data)
image = Image.open(io.BytesIO(image_bytes))

# Display the image in Jupyter
display(image)

# Close the driver
driver.quit()
