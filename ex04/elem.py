#   42 KKIM - DJANGO & PYThON PISCINE - HEADER
#		finish date: 7/30
#		passed date:
class		Text(str):

	def		__str__(self):
			return super().__str__().replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace('\n', '\n<br />\n')

class		Elem:

	class	ValidationError(Exception):
		def	__init__(self):
			super().__init__("incorrect behaviour.")
	
	def		__init__(self, tag: str = 'div', attr: dict = {}, content=None, tag_type: str = 'double'):
		self.tag = tag
		self.attr = attr
		self.content = []
		if not (self.check_type(content) or content is None):
			raise self.ValidationError
		if type(content) == list:
			self.content = content
		elif content is not None:
			self.content.append(content)
		if (tag_type != 'double' and tag_type != 'simple'):
			raise self.ValidationError
		self.tag_type = tag_type
	
	def		__str__(self):
		attr = self.make_attr()
		rest = "<{tag}{attr}".format(tag=self.tag, attr=attr)
		if self.tag_type == 'double':
			rest += ">{content}</{tag}>".format(content=self.make_content(), tag=self.tag)
		elif self.tag_type == 'simple':
			rest += " />"
		return rest
	
	def		make_attr(self):
		rest = ''
		for pair in sorted(self.attr.items()):
			rest += ' ' + str(pair[0]) + '="' + str(pair[1]) + '"'
		return rest
	
	def		make_content(self):
		if len(self.content) == 0:
			return ""
		rest = "\n"
		for elem in self.content:
			if (len(str(elem)) != 0):
				rest += "{elem}\n".format(elem=elem)
		rest = "  ".join(line for line in rest.splitlines(True))
		if len(rest.strip()) == 0:
			return ''
		return rest
	
	def		add_content(self, content):
		if not Elem.check_type(content):
			raise Elem.ValidationError
		if type(content) == list:
			self.content += [elem for elem in content if elem != Text('')]
		elif content != Text(''):
			self.content.append(content)

	@staticmethod
	def		check_type(content):
		return (
			isinstance(content, Elem) or
			type(content) == Text or
			(type(content) == list and
				all([
					type(elem) == Text or
					isinstance(elem, Elem) for elem in content])))

if __name__ == '__main__':
	html = Elem('html',
		content=[
			Elem('head',
				content=
					Elem('title',
						content=
							Text('"Hello ground!"'))),
			Elem('body',
				content=
					[
						Elem('h1',
							content=
								Text('"Oh, no, not again!"')),
						Elem('img',
							{'src': 'http://i.imgur.com/pfp3T.jpg'}, tag_type='simple')
					]
			)
		]
	)
	print(html)