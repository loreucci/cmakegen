#include <{{library}}/{{filename}}.h>

#include <gtest/gtest.h>

TEST(Test{{filename | capitalize}}, {{filename}}_function) {

    EXPECT_EQ({% if namespace is not none %}{{namespace}}::{% endif %}{{filename}}_function(2, 5), 7);

}