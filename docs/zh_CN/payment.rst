.. _payment:


******************************
构建一个付款事务
******************************

付款
=======

在下面这个示例中，你需要先确保收款账户已经在 Stellar 网络中激活了。
你可以使用同步方法在此处提交这个事务，也可以使用异步方法提交这个事务。

.. literalinclude:: ../../examples/payment.py
   :language: python
   :linenos:

路径付款(Path Payment)
========================

在下面这个示例中，我们将使用付款账户 *GABJLI6IVBKJ7HIC5NN7HHDCIEW3CMWQ2DWYHREQQUFWSWZ2CDAMZZX4* 向 *GBBM6BKZPEHWYO3E3YKREDPQXMS4VK35YLNU7NFBRI26RAN7GI5POFBB* 发送
5.5 个由 *GASOCNHNNLYFNMDJYQ3XFMI7BYHIOCFW3GJEOWRPEGK2TDPGTG2E5EDW* 发行的 *GBP*，而付款账户最多会扣除 1000 XLM。以下示例资产经过了
三轮交换：XLM->USD, USD->EUR, EUR->GBP。

* *USD* 由 *GBBM6BKZPEHWYO3E3YKREDPQXMS4VK35YLNU7NFBRI26RAN7GI5POFBB* 发行
* *EUR* 由 *GDTNXRLOJD2YEBPKK7KCMR7J33AAG5VZXHAJTHIG736D6LVEFLLLKPDL* 发行

.. literalinclude:: ../../examples/path_payment.py
   :language: python
   :linenos: