__author__ = 'Dajakk'

from django import forms

class NodeForm( forms.Form ):
	"""Overload the __init__ operator to take a list of forms as the first input and generate the
	fields that way."""

	def __init__(self, interested_subjects, *args, **kwargs):
		super( NodeForm, self ).__init__( *args, **kwargs )
		for sub in interested_subjects:
			self.fields[sub] = forms.CharField( )
