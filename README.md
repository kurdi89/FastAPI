requirements

    Python 3.6^

to install

```bash
pip install fastapi uvicorn
# or
pip3 install fastapi uvicorn
```

to run

```bash
python ./main.py

# or

py main.py

# or with uvicorn :: hotreloading

uvicorn main:app --port=3000 --reload
```

additional dependencies

```bash
pip install jinja2 aiofiles
# or
pip3 install jinja2 aiofiles
```

- jinja (templating engine to serve HTML)
- aiofiles (to setup static files)

optional

```bash
pip3 install python-engineio python-socketio websockets
```

community

    https://gitter.im/tiangolo/fastapi?at=5e610354a157485cb475d627


---


Example 3 : other references(optional)

    - http://blog.nitishmutha.com/tensorflow/2017/01/22/TensorFlow-with-gpu-for-windows.html
    - https://blog.udacity.com/2018/04/how-to-process-images-with-tensorflow.html

commands for deep learning tenserfolw style transfer

```bash
conda activate style-transfer

# then

python evaluate.py --checkpoint ./checkpoints/rain_princess.ckpt --in-path image.png --out-path ./outputs/output_image.jpg
# or
python evaluate.py --checkpoint ./checkpoints/rain_princess.ckpt --in-path ./upload/12072022-Capture.png --out-path ./outputs/output_image.jpg

```
