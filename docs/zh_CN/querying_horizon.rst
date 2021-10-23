.. _querying_horizon:


*********************
通过 Horizon 查询数据
*********************

通过 Stellar Python SDK 你可以访问 Horizon 的各个接口。

构建请求
=========

SDK 使用 `建造者模式 <https://en.wikipedia.org/wiki/Builder_pattern>`_ 来创建请求。通过 :py:class:`Server <stellar_sdk.server.Server>` ，我们可以链式的构建一个请求。
(请参阅 `Horizon 文档 <https://developers.stellar.org/api/>`_ 来了解有哪些方法是可用的。)

.. literalinclude:: ../../examples/query_horizon.py
   :language: python
   :linenos:

当请求构建完成之后，我们可以通过调用 :py:meth:`call() <stellar_sdk.call_builder.BaseCallBuilder.call>`或 :py:meth:`stream() <stellar_sdk.call_builder.BaseCallBuilder.stream>` 以向 Horizon 发起请求。
:py:meth:`call() <stellar_sdk.call_builder.BaseCallBuilder.call>` 将会立即返回一个响应。

构建流式(Stream)请求
=====================

很多接口都能通过 :py:meth:`stream() <stellar_sdk.call_builder.BaseCallBuilder.stream>` 调用。
与 :py:meth:`call() <stellar_sdk.call_builder.BaseCallBuilder.call>` 不同，它不立刻返回结果，
而是会返回一个 EventSource。

Horizon 将会实时的返回从当前时间开始产生的数据，当然你也可以通过 :py:meth:`cursor() <stellar_sdk.call_builder.BaseCallBuilder.cursor>` 指定一个时间点。
(请参阅 `Horizon 文档 <https://developers.stellar.org/api/>`_ 了解有哪些接口支持 Stream。)

下面这个示例将会实时打印这个账户提交的事务。

.. literalinclude:: ../../examples/stream_requests.py
   :language: python
   :linenos: