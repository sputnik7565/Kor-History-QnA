# Kor-History Q & A 
History Q & A is a simple ButterBlock MRC (Machine Reading Comprehension) Model web server that will give sample questions / option to type your own question from Korean historical periods texts and extract meaning from the text. 

이 프로젝트는 버터블럭의 MRC (기계독해) 모델의 웹서버 입니다. 사용자 인터페이스를 한국역사가 들어가 있는 문맥을 이용해 제공된 샘플 문제 또는 자신의 질문을 입력하여 그 문맥에서 응답을 합니다.

Constructed using Django, a Python-based free and open-source web framework

파이썬 기반 자유 및 오픈 소스 웹 프레임워크 , Django 를 사용해 구축된 프로젝트

## Getting Started 
### Dependencies 
* Python3 + 
* Docker for containerizing applications - 에플리케이션을 컨테이너에 담기 위한 도커 
* [Requirements and Versions used](https://github.com/jennystar7703/Kor-History-QnA/blob/master/requirements.txt) for virtual environment / 가상 환경을 위한 Requirements.txt 파일 

## Usage
MRC is an essential task in Natural Language Process (NLP) that teach machines to understand answer questions using unstructured text. This web server used an MRC model as base and set up a simple question and answer with easy user interface. It requires the MRC docker image running on a virtual machine, so it will not work unless that image is running.

<details><summary><b>Show instructions</b></summary>

  1. Make a `projects` folder on local disk and extract the files into the folder 
  2. Open CMD , change directory to where the project is and make a venv (virtual environment)
  ```
  https://docs.python.org/3/library/venv.html
  ```
  3. Connect to the virtual server 
  4. Install requirements.txt 
  ```
  pip install -r requirements.txt
  ```
  5. Run Server 
  ```sh
  python manage.py runserver
  ```
  6. Open [localhost:8000](localhost:8000) or http://127.0.0.1:8000/ 
  7. Enjoy the MRC model :+1:
  

</details>

## Load it as Docker Image Without Setup 
Docker containers communicate with each other through well-defined channels and does not require of the dependencies mentioned above. 
### Executing Image 
[Download Docker Image](https://drive.google.com/drive/folders/12nN8bJTo6m6YGzMzXvKI9yZZUu2MvoVR) - manual steps is included 
