.. _building_transactions:


*********************
Building Transactions
*********************

`Transactions <https://developers.stellar.org/docs/glossary/transactions/>`_ are the commands that modify the state of the ledger.
They include sending payments, creating offers, making account configuration changes, etc.

Every transaction has a source `account <https://developers.stellar.org/docs/glossary/accounts/>`__. This is the account
that pays the `fee <https://developers.stellar.org/docs/glossary/fees/>`_ and uses up a sequence number for the transaction.

Transactions are made up of one or more `operations <https://developers.stellar.org/docs/glossary/operations/>`_.
Each operation also has a source account, which defaults to the transaction's source account.

`TransactionBuilder <https://github.com/stellar/js-stellar-base/blob/master/src/transaction_builder.js>`_
-------------------------------------------------------------------------------------------------------------

The :py:class:`TransactionBuilder <stellar_sdk.transaction_builder.TransactionBuilder>` class is used to construct new transactions.
TransactionBuilder is given an account that is used as transaction's **source account**.
The transaction will use the current sequence number of the given :py:class:`Account <stellar_sdk.account.Account>`
object as its sequence number and increments the given account's sequence number
when :py:meth:`build() <stellar_sdk.transaction_builder.TransactionBuilder.build>` is called on the TransactionBuilder.

Operations can be added to the transaction calling
:py:meth:`append_operation <stellar_sdk.transaction_builder.TransactionBuilder.append_operation>` for
each operation you wish to add to the transaction.
See :ref:`operation_list_archor` for a list of possible operations you can add.
:py:meth:`append_operation <stellar_sdk.transaction_builder.TransactionBuilder.append_operation>`
returns the current :py:class:`TransactionBuilder <stellar_sdk.transaction_builder.TransactionBuilder>`
object so you can chain multiple calls. But you don't need to call it directly,
we have prepared a lot of easy-to-use functions for you, such as
:py:meth:`append_payment_op <stellar_sdk.transaction_builder.TransactionBuilder.append_payment_op>`
can add a payment operation to the :py:class:`TransactionBuilder <stellar_sdk.transaction_builder.TransactionBuilder>`.

After adding the desired operations, call the :py:meth:`build() <stellar_sdk.transaction_builder.TransactionBuilder.build>`
method on the :py:class:`TransactionBuilder <stellar_sdk.transaction_builder.TransactionBuilder>`.
This will return a fully constructed :py:class:`TransactionEnvelope <stellar_sdk.transaction_envelop.TransactionEnvelope>`.
The transaction object is wrapped in an object called a :py:class:`TransactionEnvelope <stellar_sdk.transaction_envelope.TransactionEnvelope>`,
the returned transaction will contain
the sequence number of the source account. This transaction is unsigned.
You must sign it before it will be accepted by the Stellar network.

.. literalinclude:: ../../examples/transaction_builder.py
   :language: python
   :linenos:

Sequence Numbers
----------------

The sequence number of a transaction has to match the sequence number stored by the source account or else the transaction is invalid.
After the transaction is submitted and applied to the ledger, the source account's sequence number increases by 1.

There are two ways to ensure correct sequence numbers:


#. Read the source account's sequence number before submitting a transaction
#. Manage the sequence number locally

During periods of high transaction throughput, fetching a source account's sequence number from the network may not return
the correct value. So, if you're submitting many transactions quickly, you will want to keep track of the sequence number locally.

Adding Memos
------------

Transactions can contain a **memo** field you can use to attach additional information to the transaction. You can do this
by passing a :py:class:`Memo <stellar_sdk.memo.Memo>` object when you construct the TransactionBuilder.

There are 5 types of memos:

* :py:class:`stellar_sdk.memo.NoneMemo` - empty memo,
* :py:class:`stellar_sdk.memo.TextMemo`` - 28-byte ascii encoded string memo,
* :py:class:`stellar_sdk.memo.IdMemo`- 64-bit number memo,
* :py:class:`stellar_sdk.memo.HashMemo` - 32-byte hash - ex. hash of an item in a content server,
* :py:class:`stellar_sdk.memo.ReturnHashMemo` - 32-byte hash used for returning payments - contains hash of the transaction being rejected.

.. literalinclude:: ../../examples/transaction_builder_with_memo.py
   :language: python
   :linenos:


Transaction and TransactionEnvelope
-----------------------------------
These two concepts may make the novices unclear, but the official has given a good explanation.

Transactions are commands that modify the ledger state. Among other things, Transactions are used to send payments,
enter orders into the distributed exchange, change settings on accounts, and authorize another account to hold your
currency. If you think of the ledger as a database, then transactions are SQL commands.

Once a transaction is ready to be signed, the transaction object is wrapped in an object called a Transaction Envelope,
which contains the transaction as well as a set of signatures. Most transaction envelopes only contain a single
signature along with the transaction, but in multi-signature setups it can contain many signatures. Ultimately,
transaction envelopes are passed around the network and are included in transaction sets,
as opposed to raw Transaction objects.

