from datetime import date
from enum import Enum, auto

import pdfkit
from jinja2 import Environment, FileSystemLoader
from lorem_text import lorem


class HtmlElementType(Enum):
    """
    Mögliche Vertragskomponenten
    """
    PARAGRAPH = auto()
    GENERIC = auto()
    ADDRESSFIELD = auto()
    SIGNATURES = auto()
    TABLEROW = auto()
    TABLE = auto()
    SIDEPARAGRAPH = auto()
    HEADING = auto()
    SUBJECT = auto()
    USERHTML = auto()

    def isParagraph(item):
        return item.element_type is HtmlElementType.PARAGRAPH

    def isAddress(item):
        return item.element_type is HtmlElementType.ADDRESSFIELD

    def isGeneric(item):
        return item.element_type is HtmlElementType.GENERIC

    def isSingature(item):
        return item.element_type is HtmlElementType.SIGNATURES

    def isTable(item):
        return item.element_type is HtmlElementType.TABLE

    def isHeading(item):
        return item.element_type is HtmlElementType.HEADING

    def isSideparagraph(item):
        return item.element_type is HtmlElementType.SIDEPARAGRAPH

    def isUserHtml(item):
        return item.element_type is HtmlElementType.USERHTML

    def isSubject(item):
        return item.element_type is HtmlElementType.SUBJECT


class HtmlContent:
    def __init__(self, title="", content=None, element_type=HtmlElementType.GENERIC):
        self.title = title
        self.content = content
        self.element_type = element_type


def createComponents():
    """
    Hier werden die Komponenten des Dokumentes erstellt
    Die Reihenfolge ist wichtig!
    :return: Komponenten als Liste
    """

    # TODO: Die richtigen Daten einfügen und nutzen

    # Liste der Komponenten wird initialisiert
    elements = []

    # Das Adressfeld wird initialisiert (muss immer am Anfang stehen!)
    # Die Daten dafür müssen im content dict angepasst werden
    elements.append(HtmlContent(element_type=HtmlElementType.ADDRESSFIELD))

    # Ein Betreff  wird eingefügt
    elements.append(HtmlContent(title=lorem.words(2), element_type=HtmlElementType.SUBJECT))

    # Generische Textabsätze werden mit Überschrift hinzugefügt
    for i in range(0, 5):
        title = lorem.words(4)
        content = lorem.paragraphs(2)
        elements.append(HtmlContent(title=title, content=content, element_type=HtmlElementType.PARAGRAPH))

    # Die Zeilen einer Tabelle werden initialisiert
    table_content = []
    for i in range(0, 10):
        title = lorem.words(2)
        content = lorem.words(5)
        # Die Zeilen werden befüllt
        table_content.append(HtmlContent(title=title, content=content, element_type=HtmlElementType.TABLEROW))
    # Die Zeilen werden einer Tabelle hinzugefügt und die den Komponenten
    elements.append(HtmlContent(title="Testtabelle", content=table_content, element_type=HtmlElementType.TABLE))

    # Eine Unter-Überschrift wurd hinzugefügt
    elements.append(HtmlContent(title=lorem.words(2), element_type=HtmlElementType.HEADING))

    # Es werden Absätze mit dem Titel links und dem Inhalt rechts hinzugefügt
    for i in range(0, 5):
        title = lorem.words(2)
        content = lorem.paragraphs(1)
        elements.append(HtmlContent(title=title, content=content, element_type=HtmlElementType.SIDEPARAGRAPH))

    # Absatz vor den Unterschriften und Unterschriften
    elements.append(HtmlContent(content=lorem.paragraphs(1), element_type=HtmlElementType.PARAGRAPH))
    elements.append(HtmlContent(element_type=HtmlElementType.SIGNATURES))

    return elements


def create_contract():
    """
    Erstellt das Dokument
    Im Content übergeben werden "elements",
    diese Elements sind die Komponenten aus denen ein Dokument zusammengestellt wird
    z.B. Tabellen etc.
    Daten die in diesen Tabellen, Textelementen etc. stehen werden nicht hier übergeben sondern in
    createComponents()
    In "content" übergeben werden Daten statische Daten wie "Ansprechpartner", Firmenadresse etc.
    """
    # TODO: Statische Daten anpassen
    content = {
        'elements': createComponents(),
        'company_full_name': lorem.words(1),
        'company_addr1': lorem.words(1),
        'company_addr2': lorem.words(1),
        'name_sig_1': lorem.words(2),
        'name_sig_2': lorem.words(2),
        'datum': date.today().strftime("%d.%m.%Y"),
        'ort': lorem.words(1),
        'anspr1': lorem.words(2),
        'anspr_pr_1': lorem.words(2),
        'rec': lorem.words(2),
        'rec_addr1': lorem.words(2),
        'rec_addr2':lorem.words(2),
    }

    file_loader = FileSystemLoader('./')
    env = Environment(loader=file_loader)
    env.filters['isParagraph'] = HtmlElementType.isParagraph
    env.filters['isAddress'] = HtmlElementType.isAddress
    env.filters['isGeneric'] = HtmlElementType.isGeneric
    env.filters['isSingature'] = HtmlElementType.isSingature
    env.filters['isTable'] = HtmlElementType.isTable
    env.filters['isHeading'] = HtmlElementType.isHeading
    env.filters['isSideparagraph'] = HtmlElementType.isSideparagraph
    env.filters['isUserHtml'] = HtmlElementType.isUserHtml
    env.filters['isSubject'] = HtmlElementType.isSubject
    template = env.get_template('contract.html')
    html = template.render(content)

    options = {
        '--header-html': './header.html',
        '--footer-html': './footer.html',
        'footer-right': 'Seite [page] von [topage]',
        'footer-left': content.get("company_full_name", lorem.words(1)),
        'footer-font-size': '6',
        'footer-line': '',
        '--footer-font-name': 'Open Sans',
        '--footer-spacing': '8',
    }

    pdfkit.from_string(html, 'out.pdf', options=options, css="./contract.css")


if __name__ == '__main__':
    create_contract()
