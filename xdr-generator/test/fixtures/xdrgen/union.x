typedef int Error;
typedef int Multi;

enum UnionKey {
  ERROR,
  MULTI
};

union MyUnion switch (UnionKey type)
{
    case ERROR:
        Error error;
    case MULTI:
        Multi things<>;


};

union IntUnion switch (int type)
{
    case 0:
        Error error;
    case 1:
        Multi things<>;

};

typedef IntUnion IntUnion2;
