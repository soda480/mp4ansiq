# mp4ansiq
Neat example showing how to use mp4ansi to share lots of work across a small set of workers using a Queue.

## Build Docker Image
```bash
docker image build --build-arg http_proxy --build-arg https_proxy -t mp4ansiq:latest .
```

## Run Docker Container
```bash
docker container run --rm -it -e http_proxy -e https_proxy -v $PWD:/code mp4ansiq:latest /bin/bash
```

## Execute
```bash
python mp4ansiq.py
```
![example](https://raw.githubusercontent.com/soda480/mp4ansiq/main/mp4ansiq.gif)