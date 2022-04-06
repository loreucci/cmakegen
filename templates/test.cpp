#include <{{library}}/{{filename}}.h>

#include <gtest/gtest.h>

TEST(Test{{filename | capitalize}}, {{function}}) {

    EXPECT_EQ({% if namespace is not none %}{{namespace}}::{% endif %}{{function}}(2, 5), 7);

}