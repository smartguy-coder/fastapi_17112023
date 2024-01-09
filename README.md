# fastapi_17112023

poetry config --local virtualenvs.in-project true
poetry init   
poetry init -n

poetry add fastapi[all]
poetry add "fastapi[all]"
 poetry add pytest --dev 

 uvicorn main:app  
uvicorn main:app --port 9000 --reload 



{{ dataset }}
{{ name }}
{{ inner_dict.name }}
<br>
{{ dataset.1 }}
<br>
{{ dataset[1] }}

<br>

{% for elem in dataset %}
<p>elem - {{ elem }}</p>

{% endfor %}



{% if print_data == '555' %}

{{ print_data }}

{% elif print_data == '5' %}
kljhkjjjl

{% else %}
999999999999999
{% endif %}