from django.contrib import admin
from .models import Blogger, Post, Comment, BlockedUser
from rangefilter.filters import DateRangeFilter

# Register your models here.

class BlockedUserInline(admin.StackedInline):
    model = BlockedUser
    extra = 0
    list_display = ['user', 'blocked_user']


class BloggerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', ]
    inlines = [BlockedUserInline,]

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and obj.user == request.user:
            return True
        return False


admin.site.register(Blogger, BloggerAdmin)


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0
    list_display = ['content', 'created']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['content', 'created']
    exclude = ("author",)

    def save_model(self, request, obj, form, change):
        obj.author = Blogger.objects.get(user=request.user)
        return super().save_model(request, obj, form, change)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'post':
            if request.user.is_authenticated:
                blogger = Blogger.objects.get(user=request.user)
                blocked_by = BlockedUser.objects.filter(blocked_user=blogger.user)
                blocked_by_ids = blocked_by.values_list('user_id', flat=True)
                kwargs['queryset'] = db_field.related_model.objects.exclude(author_id__in=blocked_by_ids)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and (obj.author.user == request.user or obj.post.author == request.user):
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and (obj.author.user == request.user or obj.post.author == request.user):
            return True
        return False


admin.site.register(Comment, CommentAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author']
    inlines = [CommentInline, ]
    search_fields = ("title__contains", "content__contains")
    list_filter = (("created", DateRangeFilter), )
    exclude = ("author",)

    def save_model(self, request, obj, form, change):
        obj.author = Blogger.objects.get(user=request.user)
        return super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        blogger = Blogger.objects.get(user=request.user)
        blocked_by = BlockedUser.objects.filter(blocked_user=blogger.user)
        blocked_by_ids = blocked_by.values_list('user_id', flat=True)
        queryset = queryset.exclude(author_id__in=blocked_by_ids)
        return queryset

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and (obj.author.user == request.user):
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and (obj.author.user == request.user or request.user.is_superuser):
            return True
        return False


admin.site.register(Post, PostAdmin)


class BlockedUserAdmin(admin.ModelAdmin):
    list_display = ['user', 'blocked_user']

    exclude = ("user",)

    def save_model(self, request, obj, form, change):
        obj.user = Blogger.objects.get(user=request.user)
        return super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and (obj.user == Blogger.objects.get(user=request.user) or request.user.is_superuser):
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and (obj.user == Blogger.objects.get(user=request.user) or request.user.is_superuser):
            return True
        return False


admin.site.register(BlockedUser, BlockedUserAdmin)

