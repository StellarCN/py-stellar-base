from stellar_base.keypair import Keypair


def create_keypair_determinist_english():
    mnemonic = ('illness spike retreat truth genius clock brain pass '
                'fit cave bargain toe')
    key_pair = Keypair.deterministic(mnemonic)
    print("Public key / Account address:\n", key_pair.address().decode())
    print("Seed / Your secret to keep it on local:\n",
          key_pair.seed().decode())


if __name__ == "__main__":
    create_keypair_determinist_english()
