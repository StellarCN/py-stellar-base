.. _asynchronous:


************
Asynchronous
************

Now we have supported the use of asynchronous methods to submit transactions, py-stellar-base gives you the choice,
rather than forcing you into always writing async;
sync code is easier to write, generally safer, and has many more libraries to choose from.

The following is an example of send a payment by an asynchronous method,
the same example of using the synchronization method can be found `here <payment.html#id1>`__:

.. literalinclude:: ../../examples/payment_async.py
   :language: python
   :linenos:

The following example helps you listen to multiple endpoints asynchronously.

.. literalinclude:: ../../examples/stream_requests_async.py
   :language: python
   :linenos:
