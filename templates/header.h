#ifndef {{library|upper()}}_{{filename|upper()}}_H
#define {{library|upper()}}_{{filename|upper()}}_H


{% if namespace is not none %}
namespace {{namespace}} {

{% endif %}
int {{filename}}_function(int a, int b);
{% if namespace is not none %}

}  // namespace {{namespace}}
{% endif %}

#endif  // {{library|upper()}}_{{filename|upper()}}_H