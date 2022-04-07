#include "{{library}}/{{filename}}.h"


{% if namespace is not none %}
namespace {{namespace}} {

{% endif %}
int {{filename}}_function(int a, int b) {
    return a + b;
}
{% if namespace is not none %}

}  // namespace {{namespace}}
{% endif %}