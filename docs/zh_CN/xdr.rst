.. _xdr:

***
XDR
***

XDR，也被称为外部数据表示法(External Data Representation)，它被运用在 Stellar 网络和协议中。
总账、事务、事务结果、历史，甚至在运行节点的计算机之间传递的消息都是使用 XDR 进行编码的。

:ref:`stellar_sdk_xdr` 模块提供了完整的构建与解析 XDR 的能力。

以下示例展示了如何将 XDR 字符解析为一个 XDR 对象。

.. literalinclude:: ../../examples/parse_transaction_result_xdr.py
   :language: python
   :linenos:
