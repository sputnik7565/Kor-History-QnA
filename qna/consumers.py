from channels.generic.websocket import AsyncWebsocketConsumer  # websocket 적용을 위한 channels 모듈 임포트
import json  # json 모듈
import requests  # 버터블럭 MRC에 데이터를 post 및 response 받기 위한 requests 모듈
import time  # 진행 시간 체크를 위한 time 모듈
import datetime  # 로그 파일 저장에 쓸 날짜를 받기 위한 datetime 모듈
import os  # 로그 파일 저장시 폴더 및 파일 접근을 위한 os 모듈


# 웹 소켓 연결시 실행될 클래스
class AnswerConsumer(AsyncWebsocketConsumer):

    # 웹 소켓 연결시 실행될 함수
    async def connect(self):
        await self.accept()

    # 웹소켓 끊어졌을 때 실행될 함수
    async def disconnect(self, close_code):
        pass

    # 웹소켓으로 'text_data'를 전달 받았을 대 실행될 함수
    async def receive(self, text_data):
        start = time.time()                           # 시간 체크 시작
        text_data_json = json.loads(text_data)        # 전달 받은 text_data 를 text_data_json 에 로드

        context = text_data_json['context']           # text_data_json 의 'context' 내용을 context 에 담음
        question = text_data_json['question']         # text_data_json 의 'question' 내용을 question 에 담음
        btn_id = text_data_json['btn_id']             # 실행 버튼의 구분을 위한 'btn_id'
        response_answer = ''                          # MRC 모델에서 response 받은 answer 데이터를 담기 위한 변수
        response_score = ''                           # MRC 모델에서 response 받은 question 데이터를 담기 위한 변수
        end_time = ''                                 # 프로세스가 끝난 시간을 담기 위한 변수
        list_context_slice_testing_data = ''          # 문장 길이별 출력을 받기 위한 변수

        # btn_id가 '1' 일 때 실행될 코드 ---------------->
        if btn_id == '1':
            list_context = [i + '. ' for i in context.split(". ")]                          # context 리스트
            for i in list_context[:]:                                                       # 리스트 수만큼 반복
                second_time = time.time()                                                   # 반복 시간 체크 시작
                dic_for_list_context = {'context': [str(list_context)],                     # dict 생성(context, question)
                                        'question': [str(question)]}
                response = requests.post("http://chank.iptime.org:8888/mrc",                # MRC 모델에 dict 전달
                                         json=dic_for_list_context)
                # response = requests.post("http://192.168.0.221:8888/mrc", json=dic_for_list_context)
                response_text = json.loads(response.text)                                   # 전달 받은 json 객체
                end_time_list_context = round(time.time() - second_time, 2)                 # 반복 시간 체크 끝
                # list_context 의 문장수, 전달 받은 답변, 점수, 걸린 시간을 qna_data_list 에 담음
                qna_data_list = '문장 수: ' + str(len(list_context)) + '\t\t' + \
                                '답변: ' + str(response_text[0]['answer'][:10]) + '\t\t\t' + \
                                '점수: ' + str(round(response_text[0]['score'], 2)) + '\t\t' + \
                                '걸린 시간: ' + str(end_time_list_context) + '\n' + \
                                '-' * 120 + '\n'
                list_context_slice_testing_data += qna_data_list
                list_context.remove(i)                              # 1회 반복이 끝날 때 마다 list_context 의 첫 문장을 지움

            # 로그 텍스트 저장 ---------------->
            with open(os.path.join('qna/logs', datetime.datetime.now().strftime('%Y-%m-%d') + ".txt"),
                      'a') as wfile:
                log_text = datetime.datetime.now().strftime(
                    '%Y-%m-%d %H:%M:%S') + "\n" + "context_length_test\n" + list_context_slice_testing_data + "\n\n\n"
                wfile.write(log_text)

        # btn_id가 '1' 이 아닐 때 실행될 코드 ---------------->
        else:
            dic_for_context = {'context': [context], 'question': [question]}            # dict 생성(context, question)
            response = requests.post("http://chank.iptime.org:8888/mrc",                # MRC 모델에 dict 전달
                                     json=dic_for_context)
            # response = requests.post("http://192.168.0.221:8888/mrc", json=dic_for_context)
            response_text = json.loads(response.text)                                   # 전달 받은 json 객체
            response_answer = response_text[0]['answer']
            response_score = round(response_text[0]['score'], 2)
            end_time = round(time.time() - start, 2)                                    # 시간 체크 끝

            # 로그 텍스트 저장 ---------------->
            with open(os.path.join('qna/logs', datetime.datetime.now().strftime('%Y-%m-%d') + ".txt"), 'a') as wfile:
                log_text = datetime.datetime.now().strftime(
                    '%Y-%m-%d %H:%M:%S') + "\n" + "context\n" + context + "\nquestion\n" + question + "\nanswer\n" + \
                           response_answer + "\n\n\n"
                wfile.write(log_text)

        # 프로세스 진행 후 데이터를 json 형태로 소켓에 전달 ----------------->
        await self.send(text_data=json.dumps({
            'context': context,                                                  # 지문 내용
            'question': question,                                                # 질의 내용
            'response_answer': response_answer,                                  # 답변 내용
            'response_score': response_score,                                    # 답변 점수
            'end_time': end_time,                                                # 진행 시간
            'list_context_slice_testing_data': list_context_slice_testing_data,  # 반복 실행시 생성된 데이터
            'btn_id': btn_id,                                                    # 버튼 아이디
        }))
