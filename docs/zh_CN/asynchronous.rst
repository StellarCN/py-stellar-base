.. _asynchronous:


********
异步请求
********

现在我们支持通过异步请求来提交事务了，当然我们不会强迫你使用异步，毕竟同步代码更容易编写，也有着更多的开发库可以选择。

下面这个示例演示了如何通过异步请求发起一笔付款，你可以与 `这个示例 <payment.html#id1>`__ 进行对比，
它们的功能是完全相同的，只是后者发起的是同步请求。

.. literalinclude:: ../../examples/payment_async.py
   :language: python
   :linenos:

下面这个示例演示了如何通过异步的监听多个端点。

.. literalinclude:: ../../examples/stream_requests_async.py
   :language: python
   :linenos:
