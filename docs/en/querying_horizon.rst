.. _querying_horizon:


****************
Querying Horizon
****************

py-stellar-base gives you access to all the endpoints exposed by Horizon.

Building requests
=================

py-stellar-base uses the `Builder pattern <https://en.wikipedia.org/wiki/Builder_pattern>`_ to create the requests to send
to Horizon. Starting with a :py:class:`Server <stellar_sdk.server.Server>` object, you can chain methods together to generate a query.
(See the `Horizon reference <https://developers.stellar.org/api/>`_ documentation for what methods are possible.)

.. literalinclude:: ../../examples/query_horizon.py
   :language: python
   :linenos:

Once the request is built, it can be invoked with :py:meth:`call() <stellar_sdk.call_builder.BaseCallBuilder.call>` or
with :py:meth:`stream() <stellar_sdk.call_builder.BaseCallBuilder.stream>`.
:py:meth:`call() <stellar_sdk.call_builder.BaseCallBuilder.call>` will return the
response given by Horizon.

Streaming requests
==================

Many requests can be invoked with :py:meth:`stream() <stellar_sdk.call_builder.BaseCallBuilder.stream>`.
Instead of returning a result like :py:meth:`call() <stellar_sdk.call_builder.BaseCallBuilder.call>` does,
:py:meth:`stream() <stellar_sdk.call_builder.BaseCallBuilder.stream>` will return an EventSource.
Horizon will start sending responses from either the beginning of time or from the point
specified with :py:meth:`cursor() <stellar_sdk.call_builder.BaseCallBuilder.cursor>`.
(See the `Horizon reference <https://developers.stellar.org/api/>`_ documentation to learn which endpoints support streaming.)

For example, to log instances of transactions from a particular account:

.. literalinclude:: ../../examples/stream_requests.py
   :language: python
   :linenos: