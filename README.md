[#f03c15] 위 프로젝트는 공부용으로 제작한 것이며 해당되는 내용은 악의적으로 사용하면 안됩니다. 법적인 모든 책임은 본인이 책임져야 하므로 주의바랍니다. 
# backroom
2022년 유니폭스 1학기 프로젝트로 만든 python 백도어 프로그램입니다. 예전에 만들었던 원격 제어 프로그램을 참고하여 제작하였고, 소켓과 각종 python 라이브러리들을 사용하였습니다.

# 사용법
1. server.py의 IP와 PORT를 설정합니다.<br>
![image](https://user-images.githubusercontent.com/74079392/187983387-3922733a-b9b6-4655-a4b3-e31ce594b2b5.png)<br><br>
2. 외부와 통신할 수 있도록 포트포워딩해줍니다. <br>
![image](https://user-images.githubusercontent.com/74079392/187984277-3292637c-d43d-4f37-a399-65d36a84343a.png)<br><br>
3. server.py 파일을 실행시킵니다.<br>
![image](https://user-images.githubusercontent.com/74079392/187984387-3e409bb9-52bc-4b4b-b672-7e3c9be498b2.png)
![image](https://user-images.githubusercontent.com/74079392/187984447-a27c266b-4b31-4f24-b8f6-488ed87a670a.png)<br><br>
4. 6을 눌러 client.py의 IP와 PORT를 설정합니다. 2번에서 했던 포트포워딩한 주소로 설정합니다.<br>
![image](https://user-images.githubusercontent.com/74079392/187985669-3ad29f0f-f653-4dcf-8b5f-16f8380d2e7f.png)<br><br>
5. 메뉴로 나와 8번을 눌러 exe파일을 제작합니다. (python 라이브러리 pyinstaller을 이용하였습니다.)<br>
![image](https://user-images.githubusercontent.com/74079392/187985861-5a5a40fe-ef6f-406e-b253-b047473c0313.png)<br><br>
