#/templatetags/app_filters.py
from django import template
register = template.Library()

# Calls .getlist() on a querydict
# Use: querydict | get_list {{ querydict|get_list:"itemToGet" }}
@register.filter(name='get_list')
def get_list(querydict, itemToGet ):
	return querydict.get(itemToGet)