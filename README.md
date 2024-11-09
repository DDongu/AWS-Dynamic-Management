# 충북대학교 클라우드 컴퓨팅 Term Project

AWS 동적자원관리 프로그램 (2024.11.09)

# Setting
참고: [AWS boto3 Quickstart 가이드](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html)

### 1. 필요 모듈설치

```
$ pip install boto3
```

### 2. 파일 세팅

**Windows)** _C:\Users\\[사용자명]\\.aws\credentials_

```
[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
```

**Windows)** _C:\Users\\[사용자명]\\.aws\config_

```
[default]
region=us-east-1
```