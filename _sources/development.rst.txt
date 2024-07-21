=====================
개발 가이드
=====================

이 문서는 프로젝트를 개발하기 위한 가이드입니다. 개발 환경을 설정하고, 프로젝트 구조를 이해하며, 효과적으로 기여할 수 있도록 도와줍니다.

프로젝트 설정
=============

1. 저장소 클론:
    .. code-block:: shell

        git clone https://github.com/CRA7C/SSD.git
        cd SSD

2. 필요한 의존성 설치:
    .. code-block:: shell

        python -m pip install -r requirements.txt

개발 환경
=========

의존성을 관리하기 위해 가상 환경을 사용하는 것이 좋습니다. 다음 명령어를 사용하여 가상 환경을 만들 수 있습니다:

.. code-block:: shell

    python -m venv venv
    venv\Scripts\activate  # Linux/MacOS 에서는 `source venv/bin/activate` 사용

작업을 시작하기 전에 가상 환경을 활성화하세요.

프로젝트 구조
=============

프로젝트 디렉토리 구조는 다음과 같습니다:

.. code-block:: none

    SSD/
    ├─docs/                : Sphinx doc gen. 을 위한 파일들
    ├─log/                 : logger 의 파일들을 보관하는 폴더
    ├─my_logger/           : 요구사항의 Logger 구현
    ├─ssd/                 : 가상 ssd 모듈
    ├─testapp/             : Test Shell App. 모듈
    │  ├─command/          : command 관련 하위 모듈
    │  └─scripts/          : Test Scripts 및 관련 처리 모듈
    ├─tests/               : 테스트 파일들 모음 (120개)
    │  ├─ssd_test/         : ssd 모듈의 Unit tests
    │  └─testapp_test/     : testapp 모듈의 Unit tests
    ├─requirements.txt     : 의존성 라이브러리 리스트
    └─make.bat             : make doc, make clean, make pylint 등



주요 구성 요소
==============

- `my_logger/`: 요구 된 Logger 로직을 포함합니다.
- `ssd/`: 주된 SSD(솔리드 스테이트 드라이브) 시뮬레이션 로직을 포함합니다.
- `testapp/`: SSD와 상호작용하는 테스트 애플리케이션을 포함합니다.
- `docs/`: 문서화 소스 파일을 포함합니다.
- `tests/`: 프로젝트의 테스트 케이스를 포함합니다.

코딩 스타일
=============

PEP 8, 공식 Python 스타일 가이드를 따릅니다. 코드를 이 지침에 맞추어 작성하세요. `pylint`와 `ruff` 같은 도구를 사용하여 코드를 검사하고 포맷할 수 있습니다:

.. code-block:: shell

    pylint ssd testapp
    ruff check .

테스트
========

모든 새로운 기능 및 버그 수정에는 테스트가 포함되어야 합니다. `unittest`를 사용하여 테스트를 실행합니다. 테스트를 실행하려면 다음을 사용하세요

.. code-block:: shell

    python -m unittest discover -s tests -p "*.py"

프로젝트 빌드
=============

프로젝트를 빌드하기 위해 다음 명령어를 사용할 수 있습니다:

1. 빌드 디렉토리 정리:
    .. code-block:: shell

        make clean

2. 문서화 빌드:
    .. code-block:: shell

        make doc

문서화
========

Sphinx를 사용하여 프로젝트 문서를 생성합니다. 소스 파일은 `docs/` 디렉토리에 있습니다. HTML 문서를 빌드하려면 다음을 사용하세요:

.. code-block:: shell

    make doc

기여
=======

1. 저장소를 포크하고, 기능이나 버그 수정을 위한 새 브랜치를 만드세요.
2. 변경 사항을 작성하고, 충분히 문서화하고 테스트하세요.
3. 변경 사항에 대한 명확한 설명과 함께 풀 리퀘스트를 제출하세요.

프로젝트에 기여해 주셔서 감사합니다!
