# {{ resume['name'] }}

## {{ resume['headline'] }}

## Contact Details

* Email: [{{ resume['contact']['email'] }}](mailto:{{ resume['contact']['email'] }})
* Web: [{{ resume['contact']['web']['title'] }}]({{ resume['contact']['web']['url'] }})
* GitHub: [github.com/{{ resume['contact']['github'] }}](https://github.com/{{ resume['contact']['github'] }})
* Location: [{{ resume['contact']['location']['title'] }}]({{ resume['contact']['location']['url'] }})
* [Other Formats](#other-formats)

## Summary

{{ resume['summary'] }}

## Experience
{% for job in resume['experience'] %}
### {{ job['title'] }} with {{ job['org'] }}

{{ job['start'] }} - {{ job['end'] }} - {{ job['location'] }}
{% for item in job['details'] %}
* {{ item }}
{%- endfor %}
{%- if 'tech' in job %}

Key technology and skills: _{% for skill in job['tech'] -%}
{{ skill }}
{%- if not loop.last %}, {% endif %}
{%- endfor %}_
{%- endif %}
{% endfor %}

## Education
{% for edu in resume['education'] %}
### {{ edu['school'] }}

{{ edu['degree'] }}, {{ edu['field'] }},
{{ edu['start'] }} - {{ edu['end'] }}

* Grade: {{ edu['grade'] }}
{% endfor %}

## Skills
{%- if 'strengths' in resume['skills'] %}

Key strengths: _{% for strength in resume['skills']['strengths'] -%}
{{ strength }}
{%- if not loop.last %}, {% endif %}
{%- endfor %}_
{%- endif %}

{% for skill in resume['skills']['products'] -%}
{{ skill }}
{%- if not loop.last %}, {% endif %}
{%- endfor %}

## Other Formats

* Web/HTML: <{{ resume['url'] }}/>
* PDF: <{{ resume['formats']['pdf']['url'] }}>
* Word: <{{ resume['formats']['word']['url'] }}>
* Text: <{{ resume['formats']['txt']['url'] }}>
* Narrow Text: <{{ resume['formats']['txt']['narrow_url'] }}>
* JSON: <{{ resume['formats']['json']['url'] }}>

