from django import forms
from django.utils.text import slugify
from .models import Post, Category, Tag

# Dropdown for selecting a predefined category
class PostForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all().order_by("name"),
        required=False,
        empty_label="Choose a category",
        widget=forms.Select(attrs={"class": "form-control"})
    )

    # Text input where users can type tags manually
    tags_text = forms.CharField(
        required=False,
        label="Tags",
        help_text="Separate tags with commas. Example: django, pbd, security",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "django, pbd, security"
        })
    )

    class Meta:
        model = Post
        fields = ["title", "content", "category"]
        # Styling inputs so they display properly in the form
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 6}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # When editing a post, load existing tags into the input box
        if self.instance.pk:
            self.fields["tags_text"].initial = ", ".join(
                self.instance.tags.values_list("name", flat=True)
            )

    def save(self, commit=True):
        # Save the main post first
        post = super().save(commit=commit)

        # Convert comma-separated text into Tag objects
        tag_names = [
            tag.strip()
            for tag in self.cleaned_data.get("tags_text", "").split(",")
            if tag.strip()
        ]

        tags = []
        for name in tag_names:
            # Create tag if it doesn't exist
            tag, created = Tag.objects.get_or_create(name=name)

            # Ensure slug exists for filtering
            if created and not tag.slug:
                tag.slug = slugify(name)
                tag.save()
            tags.append(tag)

        # Link tags to the post
        if commit:
            post.tags.set(tags)

        return post