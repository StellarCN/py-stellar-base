.. _asynchronous:


************
Asynchronous
************

Now we have supported the use of asynchronous methods to submit transactions, py-stellar-sdk gives you the choice,
rather than forcing you into always writing async;
sync code is easier to write, generally safer, and has many more libraries to choose from.

:py:class:`Server <stellar_sdk.server.Server>` has one parameter is **client**, here we need to talk about
the **client** parameter, if you do not specify the client, we will use
the :class:`RequestsClient <stellar_sdk.client.requests_client.RequestsClient>` instance by default,
it is a synchronous HTTPClient, you can also specify an asynchronous HTTP Client,
for example: :class:`AiohttpClient <stellar_sdk.client.aiohttp_client.AiohttpClient>`. If you use a synchronous client,
then all requests are synchronous, if you use an asynchronous client,
then all requests are asynchronous.

The following is an example of send a payment by an asynchronous method,
the same example of using the synchronization method can be found `here <payment.html#id1>`__:

.. literalinclude:: ../examples/payment_async.py
   :language: python
   :linenos:

The following example helps you listen to multiple endpoints asynchronously.

.. literalinclude:: ../examples/stream_requests_async.py
   :language: python
   :linenos:
