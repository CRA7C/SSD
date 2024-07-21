# SSD 프로젝트

**Project**: SSD Project
**Authors**: [김의윤](mailto:geniuskey@gmail.com), [박병준](mailto:qazws9346@gmail.com), [여인표](mailto:winsowss@hanmail.net), [정우훈](mailto:jwh1308@gmail.com), [하종희](mailto:gk1whd2@gmail.com)

## 개요

이 프로젝트는 가상 SSD 모듈과 Test Shell 애플리케이션을 포함한 Python 프로젝트입니다. 프로젝트는 SSD의 동작을 시뮬레이션하고, 다양한 명령어를 통해 SSD의 동작을 테스트할 수 있는 기능을 제공합니다.


## 설치

프로젝트를 설치하려면 다음 명령어를 실행하십시오:


```shell
git clone https://github.com/CRA7C/SSD.git
cd SSD
```

## 사용법

Test Shell 애플리케이션을 실행하려면 다음 명령어를 사용하십시오:

```shell
python -m testapp
```

## Test Shell 명령어

다음은 Test Shell 애플리케이션에서 사용할 수 있는 명령어 목록입니다:

- write: SSD 데이터 쓰기
- read: SSD 데이터 읽기
- exit: TestShellApplication 종료
- help: Help 보기
- fullwrite: SSD 데이터를 특정 값으로 일괄 쓰기
- fullread: SSD 데이터 전체 읽기
- erase: SSD 데이터 지우기 (LBA ~ LBA + SIZE)
- erase_range: SSD 데이터 지우기 (Start LBA ~ End LBA)


## 라이센스

이 프로젝트는 MIT 라이센스를 따릅니다. 자세한 내용은 LICENSE 파일을 참조하십시오.
