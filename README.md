# temp
___
## m1에서 Tensorflow-MacOS 설치  
[참고](https://gmnam.tistory.com/271)  
tensorflow 의존성 설치
```
conda install -c apple tensorflow-deps
```
tensroflow 설치
```
pip install tensorflow
# python -m pip install tensorflow-macos
```
metal 플러그인 설치
```
pip install tensorflow-metal
```

___
## anaconda 가상환경 제거
```
conda env remove -n '가상환경 이름'
```
___
## pip 업데이트
```
pip install --upgrade pip
```


___
https://paperswithcode.com/ 
__
## jupyter notebook 실행오류
> ImportError: cannot import name 'constants' from partially initialized module 'zmq.backend.cython' (most likely due to a circular import) (C:\Users\minho\anaconda3\envs\kaggle\lib\site-packages\zmq\backend\cython\__init__.py)
- 해결
  ```
  pip uninstall pyzmq
  pip install pyzmq
  ```
