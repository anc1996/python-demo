from PIL import ImageOps
from django.db import models
from django.utils.safestring import mark_safe
from wagtail import hooks
from wagtail.search import index
from wagtail.images.models import AbstractImage, AbstractRendition, Image
from wagtail.images.image_operations import FilterOperation


class CustomImage(AbstractImage):
    alternative_text = models.CharField(
        blank=True,
        max_length=200,
        help_text=mark_safe(
            "Provide a text alternative for this image for visually "
            "impaired users."
            "<br />For advice and best practice, visit "
            "<a href='https://moz.com/learn/seo/alt-text' target='_blank' "
            "rel='noreferrer noopener'>"
            "https://moz.com/learn/seo/alt-text</a>"
        ),
    )

    admin_form_fields = Image.admin_form_fields + (
        "alternative_text",
    )

    search_fields = AbstractImage.search_fields + [index.SearchField("alternative_text")]


class Rendition(AbstractRendition):
    image = models.ForeignKey(
        "CustomImage", related_name="renditions", on_delete=models.CASCADE
    )

    class Meta:
        unique_together = (("image", "filter_spec", "focal_point_key"),)

    @property
    def object_position_style(self):
        """
        返回一个 'object-position' 规则，以添加到 img 元素的内联样式属性中。
        类似的代码用于 wagtail image 的 background_position_style 方法。
        Reference: https://github.com/wagtail/wagtail/blob/845a2acb365241643c2f453e4b962a586ae5e713/wagtail/images/models.py#L1229
        """
        focal_point = self.focal_point
        if focal_point:
            horz = int((focal_point.x * 100) // self.width)
            vert = int((focal_point.y * 100) // self.height)
            return f"object-position: {horz}% {vert}%;"
        else:
            return "object-position: 50% 50%;"


class GrayscaleOperation(FilterOperation):
    def construct(self):
        pass

    def run(self, willow, image, env):
        willow.image = ImageOps.grayscale(willow.image)
        return willow


@hooks.register("register_image_operations")
def register_image_operations():
    return [
        ("gray", GrayscaleOperation),
    ]
