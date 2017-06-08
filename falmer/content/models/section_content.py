from django.db import models
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, TabbedInterface, StreamFieldPanel, ObjectList

from falmer.content.blocks import ContactBlock, SectionBlock


class SectionContentPage(Page):
    body = StreamField([
        ('section', SectionBlock()),
    ])

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]

    contents_in_sidebar = models.BooleanField(default=True)

    sidebar_body = StreamField([
        ('paragraph', blocks.RichTextBlock()),
        ('contact', ContactBlock()),
    ])

    sidebar_content_panels = [
        FieldPanel('contents_in_sidebar'),
        StreamFieldPanel('sidebar_body'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(sidebar_content_panels, heading='Sidebar content'),
        ObjectList(Page.promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings', classname="settings"),
    ])