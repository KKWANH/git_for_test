#   42 KKIM - DJANGO & PYThON PISCINE - HEADER
#		finish date: 7/30
#		passed date:
from	elements import	Html, Head, Body, Title, Meta, Img, Table, Th, Tr, Td, Ul, Ol, Li, H1, H2, P, Div, Span, Hr, Br, Elem, Text

class	Page:

	def	__init__(self, elem: Elem()):
		if not isinstance(elem, Elem):
			raise Elem.ValidationError()
		self.elem = elem
	
	def	__str__(self):
		result = ""
		if isinstance(self.elem, Html):
			result += "<!DOCTYPE html>\n"
		result += str(self.elem)
		return result
	
	def	write_to_file(self, path: str):
		file = open(path, "w")
		file.write(self.__str__())
	
	def	is_valid(self):
		return self.recursive_check(self.elem)
	
	def recursive_check(self, elem: Elem()):
		if not (isinstance(elem, (Html, Head, Body, Title, Meta, Img, Table, Th, Tr, Td, Ul, Ol, Li, H1, H2, P, Div, Span, Hr, Br)) \
				or type(elem) == Text):
			return False
		if type(elem) == Text or isinstance(elem, Meta):
			return True
		if isinstance(elem, Html) \
				and len(elem.content) == 2 \
				and type(elem.content[0]) == Head \
				and type(elem.content[1]) == Body:
			if (all(self.recursive_check(el) for el in elem.content)):
				return True
		elif isinstance(elem, Head) \
				and [isinstance(el, Title) for el in elem.content].count(True) == 1:
			if (all(self.recursive_check(el) for el in elem.content)):
				return True
		elif isinstance(elem, (Body, Div)) \
				and all([isinstance(el, (H1, H2, Div, Table, Ul, Ol, Span)) \
				or type(el) == Text for el in elem.content]):
			if (all(self.recursive_check(el) for el in elem.content)):
				return True
		elif isinstance(elem, (Title, H1, H2, Li, Th, Td)) \
				and len(elem.content) == 1 \
				and type(elem.content[0]) == Text:
			return True
		elif isinstance(elem, P) \
				and all([isinstance(el, Text) for el in elem.content]):
			return True
		elif isinstance(elem, Span) \
				and all([isinstance(el, (Text, P)) for el in elem.content]):
			if (all(self.recursive_check(el) for el in elem.content)):
				return True
		elif isinstance(elem, (Ul, Ol)) \
				and len(elem.content) > 0 \
				and all([isinstance(el, Li) for el in elem.content]):
			if (all(self.recursive_check(el) for el in elem.content)):
				return True
		elif isinstance(elem, Tr) \
				and len(elem.content) > 0 \
				and all([isinstance(el, (Th, Td)) for el in elem.content]) \
				and all([type(el) == type(elem.content[0]) for el in elem.content]):
			return True
		elif isinstance(elem, Table) \
				and all([isinstance(el, Tr) for el in elem.content]):
			return True
		return False



def	printtest(target: Page, toBe: bool):
	print("- - - - - - - - Start - - - - - - - -")
	print(str(target))
	print("- - - - - - - - IsValid - - - - - - -")
	assert target.is_valid() == toBe
	print("{0}".format(str(target.is_valid())))
	print("- - - - - - - - End - - - - - - - - -\n\n")

def test_Table():
	print("\n=============== {0} ===============\n".format("Table"))
	target = Page(Table())
	printtest(target, True)
	target = Page(
		Table(
			[
				Tr(),
			]))
	printtest(target, True)
	target = Page(
		Table(
			[
				H1(
					Text("Hello World!")
				),
			]))
	printtest(target, False)

def test_Tr():
	print("\n%{0}%\n".format("Tr"))
	target = Page(Tr())
	printtest(target, False)
	target = Page(
		Tr(
			[
				Th(Text("title")),
				Th(Text("title")),
				Th(Text("title")),
				Th(Text("title")),
				Th(Text("title")),
			]))
	printtest(target, True)
	target = Page(
		Tr(
			[
				Td(Text("content")),
				Td(Text("content")),
				Td(Text("content")),
				Td(Text("content")),
				Td(Text("content")),
				Td(Text("content")),
			]))
	printtest(target, True)
	target = Page(
		Tr(
			[
				Th(Text("title")),
				Td(Text("content")),
			]))
	printtest(target, False)

def test_Ul_Ol():
	print("\n%{0}%\n".format("Ul_OL"))
	target = Page(
		Ul()
	)
	printtest(target, False)
	target = Page(
		Ol()
	)
	printtest(target, False)
	target = Page(
		Ul(
			Li(
				Text('test')
			)
		)
	)
	printtest(target, True)
	target = Page(
		Ol(
			Li(
				Text('test')
			)
		)
	)
	printtest(target, True)
	target = Page(
		Ul([
			Li(
				Text('test')
			),
			Li(
				Text('test')
			),
		])
	)
	printtest(target, True)
	target = Page(
		Ol([
			Li(
				Text('test')
			),
			Li(
				Text('test')
			),
		])
	)
	printtest(target, True)
	target = Page(
		Ul([
			Li(
				Text('test')
			),
			H1(
				Text('test')
			),
		])
	)
	printtest(target, False)
	target = Page(
		Ol([
			Li(
				Text('test')
			),
			H1(
				Text('test')
			),
		])
	)
	printtest(target, False)

def test_Span():
	print("\n%{0}%\n".format("Span"))
	target = Page(
		Span()
	)
	printtest(target, True)
	target = Page(
		Span([
			Text("Hello?"),
			P(Text("World!")),
		])
	)
	printtest(target, True)
	target = Page(
		Span([
			H1(Text("World!")),
		])
	)
	printtest(target, False)


def test_P():
	print("\n%{0}%\n".format("P"))
	target = Page(
		P()
	)
	printtest(target, True)
	target = Page(
		P([
			Text("Hello?"),
		])
	)
	printtest(target, True)
	target = Page(
		P([
			H1(Text("World!")),
		])
	)
	printtest(target, False)


def test_Title_H1_H2_Li_Th_Td():
	print("\n%{0}%\n".format("H1_H2_Li_Th_Td"))
	for c in [H1, H2, Li, Th, Td]:
		target = Page(
			c()
		)
		printtest(target, False)
		target = Page(
			c([
				Text("Hello?"),
			])
		)
		printtest(target, True)
		target = Page(
			c([
				H1(Text("World!")),
			])
		)
		printtest(target, False)
		target = Page(
			c([
				Text("Hello?"),
				Text("Hello?"),
			])
		)
		printtest(target, False)


def test_Body_Div():
	print("\n%{0}%\n".format("Body_Div"))
	for c in [Body, Div]:
		target = Page(
			c()
		)
		printtest(target, True)
		target = Page(
			c([
				Text("Hello?"),
			])
		)
		printtest(target, True)
		target = Page(
			c([
				H1(Text("World!")),
			])
		)
		printtest(target, True)
		target = Page(
			c([
				Text("Hello?"),
				Span(),
			])
		)
		printtest(target, True)
		target = Page(
			c([
				Html(),
				c()
			])
		)
		printtest(target, False)


def test_Title():
	print("\n%{0}%\n".format("Title"))
	target = Page(
		Title()
	)
	printtest(target, False)
	target = Page(
		Title([
			Title(Text("Hello?")),
		])
	)
	printtest(target, True)
	target = Page(
		Title([
			Title(Text("Hello?")),
			Title(Text("Hello?")),
		])
	)
	printtest(target, False)


def test_Html():
	print("\n%{0}%\n".format("Html"))
	target = Page(
		Html()
	)
	printtest(target, False)
	target = Page(
		Html([
			Head([
				Title(Text("Hello?")),
			]),
			Body([
				H1(Text("Hello?")),
			])
		])
	)
	printtest(target, True)
	target = Page(
		Html(
			Div()
		)
	)
	printtest(target, False)


def test_Elem():
	printtest(Page(Elem()), False)

def test_write_to_file(target: Page, path: str):
	print("- - - - - - - - Start - - - - - - - -")
	print(str(target))
	print("- - - - - - - - IsValid - - - - - - -")
	target.write_to_file(path)
	print("{0}".format(path))
	print("- - - - - - - - End - - - - - - - - -\n")

if __name__ == '__main__':
	test_Table()
	test_Tr()
	test_Ul_Ol()
	test_Span()
	test_P()
	test_Title_H1_H2_Li_Th_Td()
	test_Body_Div()
	test_Html()
	test_Elem()
	test_write_to_file(
		Page(Html([Head(Title(Text("hello world!"))),
			 Body(H1(Text("HELLO WORLD!")))])),
		"test_write_to_file.html")