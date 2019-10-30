.. _asynchronous:


********
异步请求
********

现在我们支持通过异步请求来提交事务了，当然我们不会强迫你使用异步，毕竟同步代码更容易编写，也有着更多的开发库可以选择。

:py:class:`Server <stellar_sdk.server.Server>` 有一个参数是 **client**，在这里我们有必要提及一下它，如果你不明确的设置这个参数，
那么 SDK 将默认使用 :class:`RequestsClient <stellar_sdk.client.requests_client.RequestsClient>` 的实例，它是一个同步的客户端；
当然，你也可以指定一个异步的 HTTP 客户端，例如： :class:`AiohttpClient <stellar_sdk.client.aiohttp_client.AiohttpClient>`。
如果你设置了一个异步的客户端，那么所有的请求都是异步的，反之则是同步的。

下面这个示例演示了如何通过异步请求发起一笔付款，你可以与 `这个示例 <payment.html#id1>`__ 进行对比，
它们的功能是完全相同的，只是后者发起的是同步请求。

.. literalinclude:: ../../examples/payment_async.py
   :language: python
   :linenos:

下面这个示例演示了如何通过异步的监听多个端点。

.. literalinclude:: ../../examples/stream_requests_async.py
   :language: python
   :linenos:
