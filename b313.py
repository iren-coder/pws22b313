class Tag:
    tag = ""
    toplevel = False
    is_single = False
    klass = []
    id = ""
    text = ""

    def __init__(self, tagname, klass=None, toplevel=False, is_single=False, **kwargs):
        self.tag = tagname
        self.toplevel = toplevel
        self.is_single = is_single
        self.klass = klass
        self.id = id
        self.children = []
        self.attributes = {}
        if self.klass is not None:
            self.attributes["class"] = " ".join(klass)
        for attr, value in kwargs.items():
            if "_" in attr:
                attr = attr.replace("_", "-")
            self.attributes[attr] = value

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass
        

    def __str__(self):
        attrs = []
        for attribute, value in self.attributes.items():
            attrs.append('%s="%s"' % (attribute, value))
        attrs = " ".join(attrs)
        if len(attrs) > 0:
            attrs = " " + attrs
        if self.children:
            opening = "<{tag}{attrs}>\n".format(tag=self.tag, attrs=attrs)
            internal = "%s" % self.text
            for child in self.children:
                internal += str(child)
            ending = "</%s>\n" % self.tag
            return opening + internal + ending
        else:
            if self.is_single:
                return "<{tag}{attrs}/>\n".format(tag=self.tag, attrs=attrs)
            else:
                return "<{tag}{attrs}>{text}</{tag}>\n".format(
                    tag=self.tag, attrs=attrs, text=self.text
                )

    def __iadd__(self, other):
        self.children.append(other)
        return self

class HTML(Tag):
    def __init__(self, output = None):
        self.output = output
        self.tag = "html"
        self.children = []
        self.attributes = {}
        self.toplevel = True

    def __exit__(self, *args, **kwargs):
        if self.output is not None:
            with open(self.output, "w") as fp:
                fp.write(str(self))
            print("Write to a file", self.output)
            print(self)
        else:
            print(self)

class TopLevelTag(Tag):
    def __init__(self, tag):
        self.tag = tag
        self.toplevel = True
        self.children = []
        self.attributes = {}

with HTML(output=None) as doc:
    with TopLevelTag("head") as head:
        with Tag("title") as title:
            title.text = "hello"
            head += title
        doc += head

    with TopLevelTag("body") as body:
        with Tag("h1", klass=("main-text",)) as h1:
            h1.text = "Test"
            body += h1
        with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
            with Tag("p") as paragraph:
                paragraph.text = "another test"
                div += paragraph
            with Tag("img", is_single=True, src="/icon.png", data_image="responsive") as img:
                div += img
            body += div
        doc += body