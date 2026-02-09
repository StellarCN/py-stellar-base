const from = 1;
const import = from;

typedef int pass;

enum keyword_enum {
  from = 0,
  class = 1
};

struct keyword_struct {
  pass from;
  keyword_enum return;
};

union keyword_union switch (keyword_enum from)
{
    case from:
        pass class;
    default:
        void;
};
