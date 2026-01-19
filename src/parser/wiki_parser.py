import xml.etree.ElementTree as ET


def strip_ns(tag):
    """Remove XML namespace"""
    return tag.split("}", 1)[-1]


def parse_wikipedia_dump(xml_path):
    """
    Yields (doc_id, title, raw_text)
    """

    context = ET.iterparse(xml_path, events=("end",))

    for event, elem in context:
        if strip_ns(elem.tag) != "page":
            continue

        title = ""
        raw_text = ""
        doc_id = -1

        for child in elem:
            tag = strip_ns(child.tag)

            if tag == "title":
                title = child.text or ""

            elif tag == "id":
                try:
                    doc_id = int(child.text)
                except:
                    doc_id = -1

            elif tag == "revision":
                for rev_child in child:
                    if strip_ns(rev_child.tag) == "text":
                        raw_text = rev_child.text or ""

        if doc_id != -1:
            yield doc_id, title, raw_text

        elem.clear()
