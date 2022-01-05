from django.db import connection
from django.shortcuts import render


# Create your views here.
# 인덱스 페이지 실행 함수 ------->
def index(request):
    # return HttpResponse("버터블럭 MRC: 한국 역사 질의응답 데모")
    return render(request, 'qna/index.html')


# 서브 페이지 실행 함수 ------->
def his_sub(request, context_id):

    # list_context_id = ['고구려01', '백제01', '신라01', '고려01', '조선01', '임진왜란01', '일제강점기01']
    # if context_id == 'his_01':
    #     context_id = list_context_id[0]
    # elif context_id == 'his_02':
    #     context_id = list_context_id[1]
    # elif context_id == 'his_03':
    #     context_id = list_context_id[2]
    # elif context_id == 'his_04':
    #     context_id = list_context_id[3]
    # elif context_id == 'his_05':
    #     context_id = list_context_id[4]
    # elif context_id == 'his_06':
    #     context_id = list_context_id[5]
    # else:
    #     context_id = list_context_id[6]

    # context, question 글로벌 선언
    global context, question

    # MySQL context 에서 context_id에 해당하는 데이터 추출
    try:
        cursor = connection.cursor()
        query = ("SELECT hp_context FROM context WHERE hp_txt_num = '%s'" % str(context_id))
        cursor.execute(query)
        context = cursor.fetchall()
        connection.commit()
        connection.close()
    except:
        connection.rollback()
        print("Failed Selecting in StockList")

    # MySQL question 에서 context_id에 해당하는 데이터 추출
    try:
        cursor = connection.cursor()
        query = ("SELECT ques_text FROM question WHERE hp_txt_num = '%s'" % str(context_id))
        cursor.execute(query)
        question = cursor.fetchall()
        connection.commit()
        connection.close()
    except:
        connection.rollback()
        print("Failed Selecting in StockList")

    # 추출한 context 와 question 을 각각 context_text 와 question_text 에 전달
    context_text = context[0][0]
    question_text = []
    for i in question:
        question_text.append(i[0])

    # 3개로 구분된 context 를 반영하기 위한 코드 ------->
    # 현재 URL 은 /qns/ + 도메인의 마지막 2자리를 뺀 값을 담음
    #current_url = r'/qna/' + context_id[:-2]
    current_url = r'../' + context_id[:-2]
    # 세부 URL 은 현재 URL + 01, 02, 03으로 각각 담음
    redi_url_1, redi_url_2, redi_url_3 = current_url + '01', current_url + '02', current_url + '03'

    # 세부 URL 01, 02, 03으로 이동시 버튼 활성화에 따른 컬러변경을 위한 코드
    domain_bgc = ['#4c5462', '#888888']
    if context_id[-2:] == '01':
        domain_bg = [domain_bgc[0], domain_bgc[1], domain_bgc[1]]
    elif context_id[-2:] == '02':
        domain_bg = [domain_bgc[1], domain_bgc[0], domain_bgc[1]]
    else:
        domain_bg = [domain_bgc[1], domain_bgc[1], domain_bgc[0]]

    #서브 페이지로 전달할 내용----------->
    contexts = {
        'contexts': context_text,
        'question': question_text,
        'len_question': len(question_text),
        'room_name': context_id,
        'current_url': current_url,
        'redi_url_1': redi_url_1,
        'redi_url_2': redi_url_2,
        'redi_url_3': redi_url_3,
        'domain_bg': domain_bg,
    }

    return render(request, 'qna/his_sub.html', contexts)
