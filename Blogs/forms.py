from django import forms
from .models import Post, BlockedUser


class PostForm(forms.ModelForm):
    def __int__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] ="form-control"

    class Meta:
        model = Post
        exclude = ("author",)


class BlockedUserForm(forms.ModelForm):
    def __int__(self, *args, **kwargs):
        super(BlockedUserForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] ="form-control"

    class Meta:
        model = BlockedUser
        exclude = ("user",)
