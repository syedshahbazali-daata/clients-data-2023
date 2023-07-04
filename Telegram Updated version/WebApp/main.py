import threading

from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__)

current_state = 'run'

def script_manager(state_of_script):
    if state_of_script == 'run':
        os.system('python card_checker.py')
    elif state_of_script == 'stop':
        # stop the card_checker.py script
        os.system('taskkill /f /im python.exe')
    else:
        print("Invalid state")


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        state = str(request.form['state']).lower()
        if state == 'run':
            print("Run")
            threading.Thread(target=script_manager, args=(state,)).start()




            return render_template('live.html', state=current_state)
        elif state == 'stop':
            return render_template('live.html', state=current_state)



    return render_template('live.html')

if __name__ == '__main__':
    app.run(debug=True)
