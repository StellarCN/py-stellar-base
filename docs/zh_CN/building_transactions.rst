.. _building_transactions:


********
构建事务
********

`事务 <https://developers.stellar.org/docs/glossary/transactions/>`_ 是修改账本的命令，事务中一般包含了付款、创建订单、配置账户等操作。

每个事务都有一个源 `账户 <https://developers.stellar.org/docs/glossary/accounts/>`__，这个帐号将会为这笔事务支付 `手续费 <https://stellar.org/developers/learn/concepts/fees.html>`_，且这个事务会使用源账户的序列号。

事务由一个或多个 `操作组成 <https://developers.stellar.org/docs/glossary/operations/>`_，
每个操作都有一个源账户，如果一个账户没有设置源账户的话，那么它将使用事务的源账户作为它的源账户。

`TransactionBuilder <https://github.com/stellar/js-stellar-base/blob/master/src/transaction_builder.js>`_
-------------------------------------------------------------------------------------------------------------

我们可以通过 :py:class:`TransactionBuilder <stellar_sdk.transaction_builder.TransactionBuilder>` 来构建一个新的事务。
你需要在 TransactionBuilder 中配置事务的 **源账户**。这个事务会使用给定账户(:py:class:`Account <stellar_sdk.account.Account>`)的序列号，
当你调用 :py:meth:`build() <stellar_sdk.transaction_builder.TransactionBuilder.build>` 生成一个事务时，该账户的序列号会加 1.

事务中的操作可以通过调用 :py:meth:`append_operation <stellar_sdk.transaction_builder.TransactionBuilder.append_operation>` 来添加。
你可以阅读 :ref:`operation_list_archor` 来了解 Stellar 网络中有哪些类型的操作。
:py:meth:`append_operation <stellar_sdk.transaction_builder.TransactionBuilder.append_operation>`
会返回当前的 :py:class:`TransactionBuilder <stellar_sdk.transaction_builder.TransactionBuilder>`
示例，所以你可以链式的调用它。一般来说你并不需要直接调用它，我们提供了一系列便捷的函数，我更推荐你使用这些函数，比如你可以通过
:py:meth:`append_payment_op <stellar_sdk.transaction_builder.TransactionBuilder.append_payment_op>` 向
:py:class:`TransactionBuilder <stellar_sdk.transaction_builder.TransactionBuilder>` 中添加一个付款操作。

当你添加完操作之后，你可以调用 :py:meth:`build() <stellar_sdk.transaction_builder.TransactionBuilder.build>`，
它会返回一个 :py:class:`TransactionEnvelope <stellar_sdk.transaction_envelop.TransactionEnvelope>`。
整个事务都被包装在 :py:class:`TransactionEnvelope <stellar_sdk.transaction_envelope.TransactionEnvelope>` 当中，
随后你需要使用密钥对它进行签名，只有经过正确签名的事务才会被 Stellar 网络所接受。

.. literalinclude:: ../../examples/transaction_builder.py
   :language: python
   :linenos:

序列号
----------------
事务的序列号必须与源帐户的序列号匹配，如果不匹配的话该事务会被 Stellar 网络拒绝。当一个事务生效之后，源账户的序列号会加 1。

有两种方法可以确保使用的序列号是正确的：

#. 在提交事务前从 Horizon 获取账户的序列号
#. 在本地管理事务的序列号

当你尝试快速的向 Stellar 网络提交大量事务时，从网络中获取到的序列号可能是不正确的，你应该在本地对序列号进行管理。

添加备注(Memo)
---------------

事务可以包含一个用于附加额外信息的 **memo**，当前有 5 种类型的 memo：

* :py:class:`stellar_sdk.memo.NoneMemo` - 空 memo,
* :py:class:`stellar_sdk.memo.TextMemo`` - 28-字节的 Ascii 编码的字符型 memo,
* :py:class:`stellar_sdk.memo.IdMemo`- 64-位的数字型 memo,
* :py:class:`stellar_sdk.memo.HashMemo` - 32-字节的 hash 编码的 memo,
* :py:class:`stellar_sdk.memo.ReturnHashMemo` - 32-字节的 hash 编码的 memo，用与包含退款事务的 ID.

.. literalinclude:: ../../examples/transaction_builder_with_memo.py
   :language: python
   :linenos:

事务(Transaction)与事务信封(TransactionEnvelope)
--------------------------------------------------
人们常常对这两个概念感到困惑，但是官方已经给出了非常好的解释。

事务可以视为修改账本状态的命令，事务可以被用来发送付款，创建订单、修改事务或授权其他账户持有你发行的资产。
如果将账本视为一个数据库，那么事务就是 SQL 命令。

当一个事务构建好了之后，它需要被包装到事务信封当中，事务信封可以包含事务以及签名。大多数的事务信封都只包含一个签名，但是如果用户启用了多重签名的话，
事务信封便会包含多个签名了。最终在 Stellar 网络中留存的是事务信封。
