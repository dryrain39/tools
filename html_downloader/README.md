# html_downloader

## 사용법
### 실행
```console
$ python3 html_downloader.py [BASE_URL]
```

or

```console
$ python3 html_downloader.py
```

위와 같이 실행했을 때 a 태그에서 http(s):// 로 시작하는 href 속성을 찾을 수 없으면 사용자에게 base_url 세팅을 요청합니다.

### html 입력
```
C:\playground\html_downloader>html_downloader.py
HTML 텍스트를 입력하십시오. 다 입력하셨다면 <e> 를 입력하십시오.
<a href="https://---/wp-content/uploads/2020/03/file_example_WEBP_50kB.webp" class="btn btn-orange btn-outline btn-xl page-scroll download-button">Download sample WEBP file</a> 
<a class="copy-button" title="Copy file location"><e>
```

html을 붙여넣고 `<e>` 를 입력하십시오. a 태그를 파싱하여 ./downloads 폴더에 확장자가 있는 파일만 다운로드 받습니다.
