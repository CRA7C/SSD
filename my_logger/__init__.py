"""
============================
my_logger
============================

UML Diagrams
============================

my_logger 모듈 구조
----------------------------

.. image:: /_images/my_logger/logger_classes.png


Logger 동작 (TestApp 에서의 예)
-----------------------------------------

.. image:: /_images/my_logger/logger_sequence.png

"""
from .util_log import Logger

__all__ = ['Logger']
