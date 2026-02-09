%#include "generated/FBAXDR.h"

namespace MyNamespace {

// messages
typedef opaque uint512[64];
typedef opaque uint513<64>;
typedef opaque uint514<>;
typedef string str<64>;
typedef string str2<>;

typedef opaque Hash[32];
typedef Hash Hashes1[12];
typedef Hash Hashes2<12>;
typedef Hash Hashes3<>;


typedef Hash *optHash1;
typedef Hash* optHash2;

typedef int             int1;
typedef hyper           int2;
typedef unsigned int    int3;
typedef unsigned hyper  int4;

struct MyStruct
{
    uint512 field1;
    optHash1 field2;
    int1 field3;
    unsigned int field4;
    float field5;
    double field6;
    bool field7;
};

struct LotsOfMyStructs
{
    MyStruct members<>;
};

struct HasStuff
{
  LotsOfMyStructs data;
};

enum Color {
  RED,
  BLUE = 5,
  GREEN
};

const FOO = 1244;
const BAR = FOO;

struct Nester
{
  enum {
    BLAH_1,
    BLAH_2
  } nestedEnum;

  struct {
    int blah;
  } nestedStruct;

  union switch (Color color) {
    case RED:
      void;
    default:
      int blah2;
  } nestedUnion;


};

}
