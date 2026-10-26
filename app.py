from flask import *
import blinkt  
import colorsys
import time
import numpy as np

app = Flask(__name__)

blinkt.set_brightness(0.05)

# Global flag to control the background candle thread
candle_running = False
candle_thread = None

def run_candle():
    global candle_running
    start = 0
    end = 40
    i = 0
    
    # Loop runs until it finish or until cnale_running is toggled to false
    while i < 240 and candle_running:
        wait = np.random.choice(np.random.noncentral_chisquare(5, 1, 1000), 1)[0] / 50
        n = np.random.choice(np.random.noncentral_chisquare(5, 0.1, 1000), 1)
        limit = int(n[0])

        if limit > blinkt.NUM_PIXELS:
            limit = blinkt.NUM_PIXELS

        blinkt.clear()
        candle_flicker = np.random.uniform(0.3, 1.0)

        for pixel in range(limit):
            hue = start + (((end - start) / float(blinkt.NUM_PIXELS)) * pixel)
            r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(hue / 360.0, 1.0, candle_flicker)]
            blinkt.set_pixel(pixel, r, g, b)

        blinkt.show()
        time.sleep(wait)
        i += 1
    
    # Clean up and ensure everything turns off cleanly when exiting the loop
    candle_running = False
    blinkt.clear()
    blinkt.show()

@app.route("/")
def home():
    return render_template('index.html')

@app.route('/candle')
def candle():
    global candle_running, candle_thread
    
    # Only start a new candle thread if one isn't already running
    if not candle_running:
        candle_running = True
        candle_thread = threading.Thread(target=run_candle)
        candle_thread.start()
        
    return render_template('index.html')

@app.route('/off')
def off():
    global candle_running
    # Instantly signals the loop in the theard to break and exit
    candle_running = False
    
    # Hadrware backup check to forcr clear the pixels immediately    
    blinkt.clear() 
    blinkt.show()
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
