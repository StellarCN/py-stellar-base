from stellar_base.keypair import Keypair
from stellar_base.utils import StellarMnemonic


def generate_random_keypair():
    print("Generate random keypair")
    keypair = Keypair.random()
    print("Public key / Account address:\n", keypair.address().decode())
    print("Seed / Your secret to keep it on local:\n",
          keypair.seed().decode())


def create_keypair_determinist_english():
    print("Create keypair determinist english")
    mnemonic = ('illness spike retreat truth genius clock brain pass '
                'fit cave bargain toe')
    keypair = Keypair.deterministic(mnemonic)
    print("Public key / Account address:\n", keypair.address().decode())
    print("Seed / Your secret to keep it on local:\n",
          keypair.seed().decode())


def create_multiple_keypair():
    print("Create multiple keypair")
    sm = StellarMnemonic()
    secret_phrase = sm.generate()
    kp0 = Keypair.deterministic(secret_phrase, index=0)
    kp1 = Keypair.deterministic(secret_phrase, index=1)
    kp2 = Keypair.deterministic(secret_phrase, index=2)
    for keypair in (kp0, kp1, kp2):
        print("Public key / Account address:\n", keypair.address().decode())
        print("Seed / Your secret to keep it on local:\n",
              keypair.seed().decode())


if __name__ == "__main__":
    generate_random_keypair()
    create_keypair_determinist_english()
    create_multiple_keypair()
