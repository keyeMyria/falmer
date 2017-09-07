from graphene_django import DjangoObjectType, DjangoConnectionField as _DjangoConnectionField
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.rich_text import expand_db_html
from taggit.managers import TaggableManager
import graphene
from graphene_django.converter import convert_django_field
from falmer.auth import models as auth_models
from falmer.studentgroups import models as student_groups_models
from falmer.events import models as event_models
from falmer.matte.models import MatteImage


class DjangoConnectionField(_DjangoConnectionField):

    """
    Temporary fix for select_related issue
    """

    @classmethod
    def merge_querysets(cls, default_queryset, queryset):
        """
        This discarded all select_related and prefetch_related:
        # return default_queryset & queryset
        """
        return queryset

@convert_django_field.register(StreamField)
def convert_stream_field(field, registry=None):
    return "hello there"


@convert_django_field.register(TaggableManager)
def convert_taggable_manager(field, registry=None):
    return "hello there"


class Image(DjangoObjectType):
    resource = graphene.String()

    def resolve_resource(self, args, context, info):
        return self.file.name

    class Meta:
        model = MatteImage


class Venue(DjangoObjectType):

    class Meta:
        model = event_models.Venue


class Category(DjangoObjectType):

    class Meta:
        model = event_models.Category


class Type(DjangoObjectType):

    class Meta:
        model = event_models.Type


class BrandingPeriod(DjangoObjectType):

    class Meta:
        model = event_models.BrandingPeriod


class Bundle(DjangoObjectType):

    class Meta:
        model = event_models.Bundle


class Event(DjangoObjectType):
    venue = graphene.Field(Venue)
    featured_image = graphene.Field(Image)
    category = graphene.Field(Category)
    type = graphene.Field(Type)
    brand = graphene.Field(BrandingPeriod)
    bundle = graphene.Field(Bundle)
    body_html = graphene.String()
    event_id = graphene.Int()

    class Meta:
        model = event_models.Event
        interfaces = (graphene.relay.Node, )

    def resolve_body_html(self, args, context, info):
        return expand_db_html(self.body)

    def resolve_event_id(self, args, context, info):
        return self.pk


class MSLStudentGroup(DjangoObjectType):
    logo = graphene.Field(Image)

    class Meta:
        model = student_groups_models.MSLStudentGroup


class StudentGroup(DjangoObjectType):
    msl_group = graphene.Field(MSLStudentGroup)

    class Meta:
        model = student_groups_models.StudentGroup

    def resolve_msl_group(self, args, context, info):
        try:
            return self.msl_group
        except student_groups_models.MSLStudentGroup.DoesNotExist:
            return None


class ClientUser(DjangoObjectType):
    name = graphene.String()
    has_cms_access = graphene.Boolean()

    class Meta:
        model = auth_models.FalmerUser

    def resolve_name(self, args, context, info):
        return self.get_full_name()

    # this is a quick hack until we work on permissions etc
    def resolve_has_cms_access(self, args, context, info):
        return self.has_perm('wagtailadmin.access_admin')


class SearchResult(graphene.Interface):
    pass



class EventFilter(graphene.InputObjectType):
    brand_id = graphene.Int()
    from_time = graphene.String()
    to_time = graphene.String()


class Query(graphene.ObjectType):
    all_events = DjangoConnectionField(Event, filter=graphene.Argument(EventFilter))
    event = graphene.Field(Event, eventId=graphene.Int())
    # search = graphene.List(SearchResult)
    viewer = graphene.Field(ClientUser)
    all_groups = graphene.List(StudentGroup)

    def resolve_all_events(self, args, context, info):
        qs = event_models.Event.objects.select_related('featured_image', 'venue').order_by('start_time')

        qfilter = args.get('filter')

        if qfilter is None:
            return qs

        if 'from_date' in qfilter:
            qs = qs.filter(end_time__gte=qfilter['from_time'])

        if 'to_time' in qfilter:
            qs = qs.filter(start_time__lte=qfilter['to_time'])

        if 'brand_id' in qfilter:
            qs = qs.filter(brand=qfilter['brand_id'])

        return qs

    def resolve_event(self, args, context, info):
        return event_models.Event.objects.select_related('featured_image', 'bundle', 'brand').get(pk=args.get('eventId'))

    def resolve_all_groups(self, args, context, info):
        return student_groups_models.StudentGroup.objects.all()\
            .order_by('name')\
            .select_related('msl_group', 'msl_group__logo')

    def resolve_viewer(self, args, context, info):
        if context.user.is_authenticated:
            return context.user
        return None

schema = graphene.Schema(query=Query)
