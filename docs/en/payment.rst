.. _payment:


******************************
Creating a payment transaction
******************************

Payment
=======

In this example, the destination account must exist.
We use synchronous methods to submit transactions here, if you want,
you can also use asynchronous methods.

.. literalinclude:: ../../examples/payment.py
   :language: python
   :linenos:

Path Payment
============

In the example below we're sending 1000 XLM (at max) from *GABJLI6IVBKJ7HIC5NN7HHDCIEW3CMWQ2DWYHREQQUFWSWZ2CDAMZZX4* to
*GBBM6BKZPEHWYO3E3YKREDPQXMS4VK35YLNU7NFBRI26RAN7GI5POFBB*. Destination Asset will be *GBP* issued by
*GASOCNHNNLYFNMDJYQ3XFMI7BYHIOCFW3GJEOWRPEGK2TDPGTG2E5EDW*. Assets will be exchanged using the following path:


* *USD* issued by *GBBM6BKZPEHWYO3E3YKREDPQXMS4VK35YLNU7NFBRI26RAN7GI5POFBB*
* *EUR* issued by *GDTNXRLOJD2YEBPKK7KCMR7J33AAG5VZXHAJTHIG736D6LVEFLLLKPDL*

The `path payment <https://developers.stellar.org/docs/start/list-of-operations/#path-payment-strict-receive>`_ will
cause the destination address to get 5.5 GBP. It will cost the sender no more than 1000 XLM.
In this example there will be 3 exchanges, XLM->USD, USD->EUR, EUR->GBP.

.. literalinclude:: ../../examples/path_payment.py
   :language: python
   :linenos: