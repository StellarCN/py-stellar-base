.. _multi_signature_account:


***********************
Multi-signature account
***********************

`Multi-signature accounts <https://developers.stellar.org/docs/glossary/multisig/>`_
can be used to require that transactions require multiple public keys to sign before they are considered valid.
This is done by first configuring your account's **threshold** levels. Each operation has a threshold level of either low, medium,
or high. You give each threshold level a number between 1-255 in your account. Then, for each key in your account, you
assign it a weight (1-255, setting a 0 weight deletes the key). Any transaction must be signed with enough keys to meet the threshold.

For example, let's say you set your threshold levels; low = 1, medium = 2, high = 3. You want to send a payment operation,
which is a medium threshold operation. Your master key has weight 1. Additionally, you have a secondary key associated with your account which has a weight of 1.
Now, the transaction you submit for this payment must include both signatures of your master key and secondary
key since their combined weight is 2 which is enough to authorize the payment operation.

In this example, we will:

* Add a second signer to the account
* Set our account's masterkey weight and threshold levels
* Create a multi signature transaction that sends a payment

.. literalinclude:: ../../examples/set_up_multisig_account.py
   :language: python
   :linenos:
