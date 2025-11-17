{% macro norm_key(expr) %}
lower(
  regexp_replace(
    regexp_replace(
      normalize(trim({{ expr }}), NFD),   -- split accents
      r'\pM', ''                          -- drop accent marks
    ),
    r'[^a-z0-9]+', '_'                    -- collapse non-alphanumerics to underscores
  )
)
{% endmacro %}
