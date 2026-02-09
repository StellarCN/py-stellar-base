typedef hyper int64;

struct MyStruct
{
    int    someInt;
    int64  aBigInt;
    opaque someOpaque[10];
    string someString<>;
    string maxString<100>;
};
