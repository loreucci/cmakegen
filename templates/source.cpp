#include "{{library}}/{{filename}}.h"


{% if namespace is not none %}
namespace {{namespace}} {

{% endif %}
int {{function}}(int a, int b) {
    return a + b;
}
{% if namespace is not none %}

}  // namespace {{namespace}}
{% endif %}