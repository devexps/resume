# {{ resume['name'] }}

## {{ resume['headline'] }}

<br/><br/>

## Contact Details

* Email: [{{ resume['contact']['email'] }}](mailto:{{ resume['contact']['email'] }})
* Web: [{{ resume['contact']['web']['title'] }}]({{ resume['contact']['web']['url'] }})
* GitHub: [github.com/{{ resume['contact']['github'] }}](https://github.com/{{ resume['contact']['github'] }})
* Location: [{{ resume['contact']['location']['title'] }}]({{ resume['contact']['location']['url'] }})
* [Other Formats](#other-formats)

<br/><br/>

## Summary

{{ resume['summary'] }}

<br/><br/>

## Work Experience
{% for job in resume['experience'] %}
### {{ job['title'] }} with {{ job['org'] }}

**{{ job['start'] }} - {{ job['end'] }} - {{ job['location'] }}**
{% for item in job['details'] %}
* {{ item }}
{%- endfor %}
{%- if 'tech' in job %}

_**Key Technologies:** 
{% for skill in job['tech'] -%}
{{ skill }}
{%- if not loop.last %}, {% endif %}
{%- endfor %}_

<br/>

{%- endif %}
{% endfor %}

<br/><br/>

## Key Skills
{% for item in resume['skills']['keys'] %}
* {{ item }}
{%- endfor %}

<br/><br/>

## Projects
{% for project in resume['projects'] %}
### {{ project['title'] }}
{% for item in project['details'] %}
* {{ item }}
{%- endfor %}

<br/>

{% endfor %}

<br/><br/>

## Education
{% for edu in resume['education'] %}
### {{ edu['school'] }}

{{ edu['degree'] }}, {{ edu['field'] }},
{{ edu['start'] }} - {{ edu['end'] }}

* Grade: {{ edu['grade'] }}
{% endfor %}

<br/><br/>

## Goals

{{ resume['goals'] }}

<br/><br/>

## Other Formats

* Web/HTML: <{{ resume['url'] }}/>
* PDF: <{{ resume['formats']['pdf']['url'] }}>
* Word: <{{ resume['formats']['word']['url'] }}>
* Text: <{{ resume['formats']['txt']['url'] }}>
* Narrow Text: <{{ resume['formats']['txt']['narrow_url'] }}>
* JSON: <{{ resume['formats']['json']['url'] }}>

