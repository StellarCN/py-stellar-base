enum UnionKey {
  ONE = 1,
  TWO = 2,
  OFFER = 3
};

typedef int Foo;

union MyUnion switch (UnionKey type)
{
    case ONE:
        struct {
            int someInt;
        } one;

    case TWO:
        struct {
            int someInt;
            Foo foo;
        } two;

    case OFFER:
        void;
};
