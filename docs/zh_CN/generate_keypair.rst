.. _generate_keypair:


**************
生成 Keypair
**************

在 Stellar 网络中，:py:class:`Keypair <stellar_sdk.keypair.Keypair>` 用来给事务签名，
:py:class:`Keypair <stellar_sdk.keypair.Keypair>` 可以包含公钥与密钥，当然也可以只包含公钥。

如果 :py:class:`Keypair <stellar_sdk.keypair.Keypair>` 中没有包含密钥，那么它不能用来签署事务。
我们可以使用密钥来创建一个 Keypair：

.. code-block:: python
   :linenos:

   from stellar_sdk import Keypair

   keypair = Keypair.from_secret("SBK2VIYYSVG76E7VC3QHYARNFLY2EAQXDHRC7BMXBBGIFG74ARPRMNQM")
   public_key = keypair.public_key  # GDHMW6QZOL73SHKG2JA3YHXFDHM46SS5ZRWEYF5BCYHX2C5TVO6KZBYL
   can_sign = keypair.can_sign()  # True


我们也可以用公钥来创建一个功能有限的 Keypair：

.. code-block:: python
   :linenos:

   from stellar_sdk import Keypair

   keypair = Keypair.from_public_key("GDHMW6QZOL73SHKG2JA3YHXFDHM46SS5ZRWEYF5BCYHX2C5TVO6KZBYL")
   can_sign = keypair.can_sign()  # False

还可以生成一个随机的 Keypair：

.. code-block:: python
   :linenos:

   from stellar_sdk import Keypair

   keypair = Keypair.random()
   print("Public Key: " + keypair.public_key)
   print("Secret Seed: " + keypair.secret)