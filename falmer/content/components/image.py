from wagtail.wagtailcore import blocks

from falmer.content.blocks import FalmerImageChooserBlock


class ImageBlock(blocks.StructBlock):
    """
    Block for single images with all necessary attributes such as alternative title, caption and so on.
    """
    image = FalmerImageChooserBlock(required=True)
    alternative_title = blocks.CharBlock(required=False)
    caption = blocks.CharBlock(required=False)

    @property
    def get_title(self):
        if self.alternative_title:
            return self.alternative_title
        else:
            self.image.title

    class Meta:
        icon = 'image'


image = ('image', ImageBlock())
